from fastapi import FastAPI, APIRouter, HTTPException, Request, Header, Response, Cookie
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
import socketio
from datetime import datetime, timezone, timedelta
import bcrypt
import urllib.parse
from hashlib import md5
# emergentintegrations is only available on Emergent platform - use fallbacks for external deployment
try:
    from emergentintegrations.llm.chat import LlmChat, UserMessage
    from emergentintegrations.payments.stripe.checkout import StripeCheckout, CheckoutSessionResponse, CheckoutStatusResponse, CheckoutSessionRequest
    HAS_EMERGENT = True
except ImportError:
    HAS_EMERGENT = False
    LlmChat = None
    UserMessage = None
    StripeCheckout = None

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Socket.IO setup
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
fastapi_app = FastAPI()
api_router = APIRouter(prefix="/api")

# ==================== MODELS ====================

class User(BaseModel):
    user_id: str = Field(default_factory=lambda: f"user_{uuid.uuid4().hex[:12]}")
    email: str
    name: str
    password_hash: Optional[str] = None
    google_id: Optional[str] = None
    phone: Optional[str] = None
    addresses: List[Dict[str, Any]] = []
    payment_methods: List[Dict[str, Any]] = []
    loyalty_points: int = 0
    preferences: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserSignup(BaseModel):
    email: str
    password: str
    name: str
    phone: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class GoogleSessionExchange(BaseModel):
    session_id: str

class Restaurant(BaseModel):
    restaurant_id: str = Field(default_factory=lambda: f"rest_{uuid.uuid4().hex[:12]}")
    name: str
    description: str
    image: str
    cuisine_type: str
    rating: float = 4.5
    delivery_time: str = "30-40 min"
    price_range: str = "$$"
    location: Dict[str, Any]
    featured: bool = False
    active: bool = True
    menu_categories: List[str] = []

class MenuItem(BaseModel):
    item_id: str = Field(default_factory=lambda: f"item_{uuid.uuid4().hex[:12]}")
    restaurant_id: str
    name: str
    description: str
    price: float
    image: str
    category: str
    available: bool = True
    dietary_tags: List[str] = []

class OrderItem(BaseModel):
    item_id: str
    name: str
    price: float
    quantity: int
    special_instructions: Optional[str] = None

class Order(BaseModel):
    order_id: str = Field(default_factory=lambda: f"order_{uuid.uuid4().hex[:12]}")
    user_id: str
    restaurant_id: str
    restaurant_name: str
    items: List[OrderItem]
    subtotal: float
    delivery_fee: float = 3.99
    tax: float
    total: float
    delivery_address: Dict[str, Any]
    payment_method: str = "card"
    order_notes: str = ""
    allergies: List[str] = []
    tip: float = 0
    promo_code: Optional[str] = None
    status: str = "pending"  # pending, confirmed, preparing, ready, picked_up, delivered, cancelled
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    estimated_delivery: Optional[datetime] = None

class CreateOrder(BaseModel):
    restaurant_id: str
    items: List[OrderItem]
    delivery_address: Dict[str, Any]
    payment_method: str = "card"
    order_notes: str = ""
    allergies: List[str] = []
    tip: float = 0
    promo_code: Optional[str] = None

class Review(BaseModel):
    review_id: str = Field(default_factory=lambda: f"review_{uuid.uuid4().hex[:12]}")
    user_id: str
    user_name: str
    restaurant_id: str
    order_id: Optional[str] = None
    rating: float
    comment: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CreateReview(BaseModel):
    restaurant_id: str
    rating: float
    comment: str
    order_id: Optional[str] = None

class UserSession(BaseModel):
    session_token: str = Field(default_factory=lambda: f"session_{uuid.uuid4().hex}")
    user_id: str
    expires_at: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class PaymentTransaction(BaseModel):
    transaction_id: str = Field(default_factory=lambda: f"txn_{uuid.uuid4().hex[:12]}")
    session_id: str
    user_id: Optional[str] = None
    amount: float
    currency: str = "usd"
    status: str = "pending"  # pending, completed, failed, expired
    payment_status: str = "initiated"  # initiated, paid, unpaid
    metadata: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AIRecommendationRequest(BaseModel):
    user_preferences: Optional[Dict[str, Any]] = None
    recent_orders: Optional[List[str]] = None

class MoodSuggestionRequest(BaseModel):
    mood: str  # comfort, healthy, quick, indulgent, etc.

# ==================== SOCKET.IO HANDLERS ====================

@sio.event
async def connect(sid, environ):
    logger.info(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    logger.info(f"Client disconnected: {sid}")

@sio.event
async def join_order_room(sid, data):
    order_id = data.get("order_id")
    if not order_id:
        logger.warning(f"join_order_room called without order_id for {sid}")
        return
    await sio.enter_room(sid, order_id)
    logger.info(f"Client {sid} joined order room {order_id}")

async def broadcast_order_update(order_id: str, order_data: dict):
    """Broadcast order status update to all clients in the order room"""
    await sio.emit('order_update', order_data, room=order_id)
    logger.info(f"Broadcasted update for order {order_id}: {order_data.get('status')}")

# ==================== AUTH HELPERS ====================

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

async def get_current_user(authorization: Optional[str] = None, session_token: Optional[str] = None) -> User:
    """Get current user from session token (cookie or header)"""
    token = session_token or (authorization.replace("Bearer ", "") if authorization else None)
    
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Find session
    session_doc = await db.user_sessions.find_one({"session_token": token}, {"_id": 0})
    if not session_doc:
        raise HTTPException(status_code=401, detail="Invalid session")
    
    # Check expiry
    expires_at = session_doc["expires_at"]
    if isinstance(expires_at, str):
        expires_at = datetime.fromisoformat(expires_at)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Session expired")
    
    # Get user
    user_doc = await db.users.find_one({"user_id": session_doc["user_id"]}, {"_id": 0})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")
    
    return User(**user_doc)

# ==================== AUTH ENDPOINTS ====================

@api_router.post("/auth/signup")
async def signup(data: UserSignup):
    """Register a new user with email and password"""
    # Check if user exists
    existing = await db.users.find_one({"email": data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    user = User(
        email=data.email,
        name=data.name,
        phone=data.phone,
        password_hash=hash_password(data.password)
    )
    
    await db.users.insert_one(user.model_dump())
    
    # Create session
    session = UserSession(
        user_id=user.user_id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=7)
    )
    await db.user_sessions.insert_one(session.model_dump())
    
    # Return user without password hash
    user_dict = user.model_dump()
    user_dict.pop('password_hash', None)
    
    return {
        "user": user_dict,
        "session_token": session.session_token
    }

@api_router.post("/auth/login")
async def login(data: UserLogin, response: Response):
    """Login with email and password"""
    # Find user
    user_doc = await db.users.find_one({"email": data.email}, {"_id": 0})
    if not user_doc:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password
    if not user_doc.get("password_hash") or not verify_password(data.password, user_doc["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user = User(**user_doc)
    
    # Create session
    session = UserSession(
        user_id=user.user_id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=7)
    )
    await db.user_sessions.insert_one(session.model_dump())
    
    # Set cookie
    response.set_cookie(
        key="session_token",
        value=session.session_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=7*24*60*60,
        path="/"
    )
    
    # Return user without password hash
    user_dict = user.model_dump()
    user_dict.pop('password_hash', None)
    
    return {
        "user": user_dict,
        "session_token": session.session_token
    }

@api_router.post("/auth/google/session")
async def google_session_exchange(data: GoogleSessionExchange, response: Response):
    """Exchange Google OAuth session_id for app session"""
    import aiohttp
    
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data",
            headers={"X-Session-ID": data.session_id}
        ) as resp:
            if resp.status != 200:
                raise HTTPException(status_code=400, detail="Invalid session ID")
            
            google_data = await resp.json()
    
    # Find or create user
    user_doc = await db.users.find_one({"email": google_data["email"]}, {"_id": 0})
    
    if user_doc:
        user = User(**user_doc)
        # Update Google ID if not set
        if not user.google_id:
            await db.users.update_one(
                {"user_id": user.user_id},
                {"$set": {"google_id": google_data["id"]}}
            )
    else:
        # Create new user
        user = User(
            email=google_data["email"],
            name=google_data.get("name", "User"),
            google_id=google_data["id"]
        )
        await db.users.insert_one(user.model_dump())
    
    # Create session
    session = UserSession(
        user_id=user.user_id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=7)
    )
    await db.user_sessions.insert_one(session.model_dump())
    
    # Set cookie
    response.set_cookie(
        key="session_token",
        value=session.session_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=7*24*60*60,
        path="/"
    )
    
    # Return user
    user_dict = user.model_dump()
    user_dict.pop('password_hash', None)
    
    return {
        "user": user_dict,
        "session_token": session.session_token
    }

@api_router.get("/auth/me")
async def get_me(
    authorization: Optional[str] = Header(None),
    session_token: Optional[str] = Cookie(None)
):
    """Get current authenticated user"""
    user = await get_current_user(authorization, session_token)
    user_dict = user.model_dump()
    user_dict.pop('password_hash', None)
    return user_dict

@api_router.post("/auth/logout")
async def logout(
    response: Response,
    authorization: Optional[str] = Header(None),
    session_token: Optional[str] = Cookie(None)
):
    """Logout and clear session"""
    token = session_token or (authorization.replace("Bearer ", "") if authorization else None)
    
    if token:
        await db.user_sessions.delete_one({"session_token": token})
    
    response.delete_cookie("session_token", path="/")
    return {"message": "Logged out successfully"}

# ==================== SERVICE ENDPOINTS ====================

@api_router.get("/services")
async def get_services():
    """Get all available service categories"""
    services = await db.services.find({"active": True}, {"_id": 0}).to_list(20)
    return services

# ==================== RESTAURANT ENDPOINTS ====================

@api_router.get("/restaurants")
async def get_restaurants(
    cuisine: Optional[str] = None,
    featured: Optional[bool] = None,
    search: Optional[str] = None,
    service_type: Optional[str] = None
):
    """Get list of restaurants with optional filters"""
    query = {"active": True}
    
    if cuisine:
        query["cuisine_type"] = cuisine
    if featured is not None:
        query["featured"] = featured
    if service_type:
        query["service_type"] = service_type
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"cuisine_type": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]
    
    restaurants = await db.restaurants.find(query, {"_id": 0}).to_list(100)
    return restaurants

@api_router.get("/restaurants/{restaurant_id}")
async def get_restaurant(restaurant_id: str):
    """Get restaurant details"""
    restaurant = await db.restaurants.find_one({"restaurant_id": restaurant_id}, {"_id": 0})
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

@api_router.get("/restaurants/{restaurant_id}/menu")
async def get_restaurant_menu(restaurant_id: str, category: Optional[str] = None):
    """Get restaurant menu items"""
    query = {"restaurant_id": restaurant_id, "available": True}
    if category:
        query["category"] = category
    
    items = await db.menu_items.find(query, {"_id": 0}).to_list(200)
    return items

@api_router.get("/restaurants/{restaurant_id}/reviews")
async def get_restaurant_reviews(restaurant_id: str, limit: int = 20):
    """Get restaurant reviews"""
    reviews = await db.reviews.find(
        {"restaurant_id": restaurant_id},
        {"_id": 0}
    ).sort("created_at", -1).limit(limit).to_list(limit)
    return reviews

# ==================== ORDER ENDPOINTS ====================

@api_router.post("/orders")
async def create_order(
    data: CreateOrder,
    authorization: Optional[str] = Header(None),
    session_token: Optional[str] = Cookie(None)
):
    """Create a new order"""
    user = await get_current_user(authorization, session_token)
    
    # Get restaurant
    restaurant = await db.restaurants.find_one({"restaurant_id": data.restaurant_id}, {"_id": 0})
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Calculate totals
    subtotal = sum(item.price * item.quantity for item in data.items)
    delivery_fee = 25.00  # R25 delivery fee per restaurant
    tax = subtotal * 0.15  # 15% VAT (South Africa)
    total = subtotal + delivery_fee + tax
    
    # Create order
    order = Order(
        user_id=user.user_id,
        restaurant_id=data.restaurant_id,
        restaurant_name=restaurant["name"],
        items=[item.model_dump() for item in data.items],
        subtotal=round(subtotal, 2),
        delivery_fee=round(delivery_fee, 2),
        tax=round(tax, 2),
        total=round(total + data.tip, 2),
        delivery_address=data.delivery_address,
        payment_method=data.payment_method,
        order_notes=data.order_notes,
        allergies=data.allergies,
        tip=data.tip,
        promo_code=data.promo_code,
        estimated_delivery=datetime.now(timezone.utc) + timedelta(minutes=40)
    )
    
    await db.orders.insert_one(order.model_dump())
    
    # Update loyalty points (1 point per dollar)
    points_earned = int(total)
    await db.users.update_one(
        {"user_id": user.user_id},
        {"$inc": {"loyalty_points": points_earned}}
    )
    
    return order.model_dump()

# ==================== PAYFAST PAYMENT INTEGRATION ====================

PAYFAST_CHECKOUT_FIELD_ORDER = [
    "merchant_id", "merchant_key", "return_url", "cancel_url", "notify_url",
    "name_first", "name_last", "email_address", "cell_number",
    "m_payment_id", "amount", "item_name", "item_description",
    "custom_int1", "custom_str1", "custom_str2",
    "email_confirmation", "confirmation_address", "payment_method",
]

def get_payfast_config():
    return {
        "merchant_id": os.getenv("PAYFAST_MERCHANT_ID", "10000100"),
        "merchant_key": os.getenv("PAYFAST_MERCHANT_KEY", "46f0cd694581a"),
        "passphrase": os.getenv("PAYFAST_PASSPHRASE", ""),
        "sandbox": os.getenv("PAYFAST_SANDBOX", "true").lower() == "true",
    }

def calculate_payfast_signature(data: dict, passphrase: str) -> str:
    """Generate PayFast MD5 signature"""
    filtered = {k: str(v).strip() for k, v in data.items() if k != 'signature' and v is not None and str(v).strip()}
    priority_dict = {k: i for i, k in enumerate(PAYFAST_CHECKOUT_FIELD_ORDER)}
    sorted_keys = sorted(filtered.keys(), key=lambda k: priority_dict.get(k, 999))
    param_str = '&'.join(f"{key}={urllib.parse.quote_plus(filtered[key])}" for key in sorted_keys)
    if passphrase:
        param_str += f"&passphrase={urllib.parse.quote_plus(passphrase)}"
    return md5(param_str.encode('utf-8')).hexdigest()

@api_router.post("/payments/payfast/create")
async def create_payfast_payment(
    request: Request,
    authorization: Optional[str] = Header(None),
    session_token: Optional[str] = Cookie(None)
):
    """Create a PayFast payment for an order"""
    user = await get_current_user(authorization, session_token)
    body = await request.json()
    order_id = body.get("order_id")

    if not order_id:
        raise HTTPException(status_code=400, detail="order_id required")

    order = await db.orders.find_one({"order_id": order_id, "user_id": user.user_id}, {"_id": 0})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    pf = get_payfast_config()
    base_url = str(request.base_url).rstrip('/')
    # Use /api prefix for callbacks
    api_base = base_url.replace(':3000', ':8001') if ':3000' in base_url else base_url

    payment_data = {
        "merchant_id": pf["merchant_id"],
        "merchant_key": pf["merchant_key"],
        "return_url": f"{base_url}/api/payments/payfast/return?order_id={order_id}",
        "cancel_url": f"{base_url}/api/payments/payfast/cancel?order_id={order_id}",
        "notify_url": f"{api_base}/api/payments/payfast/notify",
        "name_first": user.name.split()[0] if user.name else "Customer",
        "name_last": user.name.split()[-1] if user.name and len(user.name.split()) > 1 else "",
        "email_address": user.email,
        "m_payment_id": order_id,
        "amount": f"{order['total']:.2f}",
        "item_name": f"No Limit Delivery - Order {order_id[:16]}",
        "item_description": f"{len(order.get('items', []))} items from {order.get('restaurant_name', 'restaurant')}",
    }

    payment_data["signature"] = calculate_payfast_signature(payment_data, pf["passphrase"])

    payfast_url = "https://sandbox.payfast.co.za/eng/process" if pf["sandbox"] else "https://www.payfast.co.za/eng/process"

    # Update order status
    await db.orders.update_one(
        {"order_id": order_id},
        {"$set": {"status": "awaiting_payment", "payment_method": "payfast"}}
    )

    return {
        "payfast_url": payfast_url,
        "payment_data": payment_data,
        "order_id": order_id,
        "sandbox": pf["sandbox"],
    }

@api_router.post("/payments/payfast/notify")
async def payfast_itn(request: Request):
    """PayFast Instant Transaction Notification (ITN) callback"""
    try:
        form_data = await request.form()
        data = dict(form_data)
        logger.info(f"PayFast ITN received: {data}")

        pf = get_payfast_config()
        order_id = data.get("m_payment_id", "")
        payment_status = data.get("payment_status", "")

        # Verify signature
        received_sig = data.get("signature", "")
        calculated_sig = calculate_payfast_signature(data, pf["passphrase"])

        if received_sig != calculated_sig:
            logger.warning(f"PayFast signature mismatch for order {order_id}")
            # In sandbox mode, still process
            if not pf["sandbox"]:
                return Response(status_code=400, content="Signature mismatch")

        if payment_status == "COMPLETE":
            await db.orders.update_one(
                {"order_id": order_id},
                {"$set": {
                    "status": "confirmed",
                    "payment_status": "paid",
                    "payment_method": "payfast",
                    "pf_payment_id": data.get("pf_payment_id", ""),
                    "updated_at": datetime.now(timezone.utc),
                }}
            )
            logger.info(f"Order {order_id} marked as PAID via PayFast")
        elif payment_status == "CANCELLED":
            await db.orders.update_one(
                {"order_id": order_id},
                {"$set": {"status": "cancelled", "payment_status": "cancelled"}}
            )
            logger.info(f"Order {order_id} CANCELLED via PayFast")

        return Response(status_code=200, content="OK")
    except Exception as e:
        logger.error(f"PayFast ITN error: {e}")
        return Response(status_code=200, content="OK")

@api_router.get("/payments/payfast/return")
async def payfast_return(order_id: str = ""):
    """PayFast return URL - user redirected here after payment"""
    # Mark as paid (ITN may arrive later with definitive status)
    if order_id:
        await db.orders.update_one(
            {"order_id": order_id, "status": "awaiting_payment"},
            {"$set": {"status": "confirmed", "payment_status": "paid", "updated_at": datetime.now(timezone.utc)}}
        )
    return HTMLResponse(f"""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>body{{font-family:system-ui;display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0;background:#F0F2ED;text-align:center}}
    .card{{padding:40px;background:white;border-radius:16px;max-width:360px;box-shadow:0 4px 20px rgba(0,0,0,0.1)}}
    h2{{color:#333;margin-bottom:8px}}p{{color:#666}}
    .btn{{display:inline-block;margin-top:20px;padding:14px 28px;background:#87A96B;color:white;border-radius:12px;text-decoration:none;font-weight:600}}</style></head>
    <body><div class="card">
    <h2>Payment Successful!</h2>
    <p>Your order has been confirmed and is being prepared.</p>
    <p style="font-size:13px;color:#999">Order: {order_id}</p>
    <a class="btn" href="/">Back to App</a>
    </div></body></html>
    """)

@api_router.get("/payments/payfast/cancel")
async def payfast_cancel(order_id: str = ""):
    """PayFast cancel URL - user cancelled payment"""
    if order_id:
        await db.orders.update_one(
            {"order_id": order_id},
            {"$set": {"status": "payment_cancelled", "updated_at": datetime.now(timezone.utc)}}
        )
    return HTMLResponse(f"""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>body{{font-family:system-ui;display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0;background:#F0F2ED;text-align:center}}
    .card{{padding:40px;background:white;border-radius:16px;max-width:360px;box-shadow:0 4px 20px rgba(0,0,0,0.1)}}
    h2{{color:#333;margin-bottom:8px}}p{{color:#666}}
    .btn{{display:inline-block;margin-top:20px;padding:14px 28px;background:#87A96B;color:white;border-radius:12px;text-decoration:none;font-weight:600}}</style></head>
    <body><div class="card">
    <h2>Payment Cancelled</h2>
    <p>Your payment was not completed. You can try again from your orders.</p>
    <a class="btn" href="/">Back to App</a>
    </div></body></html>
    """)

@api_router.get("/orders")
async def get_orders(
    authorization: Optional[str] = Header(None),
    session_token: Optional[str] = Cookie(None)
):
    """Get user's orders"""
    user = await get_current_user(authorization, session_token)
    
    orders = await db.orders.find(
        {"user_id": user.user_id},
        {"_id": 0}
    ).sort("created_at", -1).to_list(50)
    
    return orders

@api_router.get("/orders/{order_id}")
async def get_order(
    order_id: str,
    authorization: Optional[str] = Header(None),
    session_token: Optional[str] = Cookie(None)
):
    """Get order details"""
    user = await get_current_user(authorization, session_token)
    
    order = await db.orders.find_one(
        {"order_id": order_id, "user_id": user.user_id},
        {"_id": 0}
    )
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order

@api_router.patch("/orders/{order_id}/status")
async def update_order_status(order_id: str, status: str):
    """Update order status (for testing/demo purposes)"""
    valid_statuses = ["pending", "confirmed", "preparing", "ready", "picked_up", "delivered", "cancelled"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    result = await db.orders.update_one(
        {"order_id": order_id},
        {
            "$set": {
                "status": status,
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Get updated order and broadcast
    order = await db.orders.find_one({"order_id": order_id}, {"_id": 0})
    await broadcast_order_update(order_id, order)
    
    return {"message": "Order status updated", "status": status}

# ==================== AI RECOMMENDATION ENDPOINTS ====================

@api_router.post("/ai/recommendations")
async def get_recommendations(
    data: AIRecommendationRequest,
    authorization: Optional[str] = Header(None),
    session_token: Optional[str] = Cookie(None)
):
    """Get AI-powered personalized restaurant recommendations"""
    user = await get_current_user(authorization, session_token)
    
    # Get user's order history
    recent_orders = await db.orders.find(
        {"user_id": user.user_id},
        {"_id": 0, "restaurant_name": 1, "items": 1}
    ).sort("created_at", -1).limit(5).to_list(5)
    
    # Get all restaurants
    restaurants = await db.restaurants.find({"active": True}, {"_id": 0}).to_list(50)
    
    # Prepare context for AI
    order_history = ", ".join([order["restaurant_name"] for order in recent_orders]) if recent_orders else "No previous orders"
    restaurant_list = ", ".join([f"{r['name']} ({r['cuisine_type']})" for r in restaurants[:20]])
    
    # Call LLM (only works on Emergent platform)
    if not HAS_EMERGENT:
        return {"recommendations": "Browse our 13+ local providers!", "restaurants": restaurants[:5]}
    
    chat = LlmChat(
        api_key=os.environ.get("EMERGENT_LLM_KEY"),
        session_id=f"recommendations_{user.user_id}",
        system_message="You are a food recommendation expert. Provide personalized restaurant recommendations based on user's order history and preferences."
    ).with_model("openai", "gpt-5.2")
    
    message = UserMessage(
        text=f"User's recent orders: {order_history}. Available restaurants: {restaurant_list}. Recommend 3-5 restaurants and explain why they would enjoy them. Keep it concise and friendly."
    )
    
    response = await chat.send_message(message)
    
    return {
        "recommendations": response,
        "restaurants": restaurants[:5]
    }

@api_router.post("/ai/randomizer")
async def food_randomizer():
    """What should I eat? AI randomizer"""
    # Get random restaurants
    pipeline = [
        {"$match": {"active": True}}, 
        {"$sample": {"size": 10}},
        {"$project": {"_id": 0}}
    ]
    restaurants = await db.restaurants.aggregate(pipeline).to_list(10)
    
    restaurant_list = ", ".join([f"{r['name']} ({r['cuisine_type']})" for r in restaurants])
    
    # Call LLM (only works on Emergent platform)
    if not HAS_EMERGENT:
        import random
        pick = random.choice(restaurants) if restaurants else {"name": "Pedro's Chicken", "cuisine_type": "Chicken"}
        return {"suggestion": f"Today's pick: {pick['name']}! Great {pick.get('cuisine_type', 'food')} awaits.", "restaurants": restaurants}
    
    chat = LlmChat(
        api_key=os.environ.get("EMERGENT_LLM_KEY"),
        session_id=f"randomizer_{uuid.uuid4().hex[:8]}",
        system_message="You are a fun, enthusiastic food advisor. Pick one random option and make it sound exciting!"
    ).with_model("openai", "gpt-5.2")
    
    message = UserMessage(
        text=f"From these restaurants: {restaurant_list}, pick ONE at random and tell me why I should order from there today. Be enthusiastic and fun!"
    )
    
    response = await chat.send_message(message)
    
    return {
        "suggestion": response,
        "restaurants": restaurants
    }

@api_router.post("/ai/mood-suggestions")
async def mood_suggestions(data: MoodSuggestionRequest):
    """Get mood-based food suggestions"""
    mood_contexts = {
        "comfort": "comforting, warm, satisfying comfort food",
        "healthy": "light, fresh, nutritious and healthy meals",
        "quick": "fast, convenient, ready-to-eat options",
        "indulgent": "rich, decadent, treat-yourself meals",
        "adventurous": "unique, exotic, try-something-new options"
    }
    
    mood_context = mood_contexts.get(data.mood.lower(), "delicious food")
    
    # Get restaurants
    restaurants = await db.restaurants.find({"active": True}, {"_id": 0}).to_list(30)
    restaurant_list = ", ".join([f"{r['name']} ({r['cuisine_type']})" for r in restaurants])
    
    # Call LLM (only works on Emergent platform)
    if not HAS_EMERGENT:
        return {"suggestions": f"Based on your mood, try one of our {len(restaurants)} providers!", "restaurants": restaurants[:5]}
    
    chat = LlmChat(
        api_key=os.environ.get("EMERGENT_LLM_KEY"),
        session_id=f"mood_{uuid.uuid4().hex[:8]}",
        system_message=f"You are a food mood expert. Recommend restaurants perfect for someone wanting {mood_context}."
    ).with_model("openai", "gpt-5.2")
    
    message = UserMessage(
        text=f"I'm in the mood for {mood_context}. From these restaurants: {restaurant_list}, recommend 3-5 that fit this mood perfectly. Explain why each one matches."
    )
    
    response = await chat.send_message(message)
    
    return {
        "mood": data.mood,
        "suggestions": response,
        "restaurants": restaurants[:5]
    }

# ==================== PAYMENT ENDPOINTS ====================

@api_router.post("/payments/create-checkout")
async def create_checkout(
    request: Request,
    amount: float,
    order_id: str,
    authorization: Optional[str] = Header(None),
    session_token: Optional[str] = Cookie(None)
):
    """Create Stripe checkout session"""
    if not HAS_EMERGENT:
        raise HTTPException(status_code=501, detail="Stripe not available. Use PayFast instead.")
    user = await get_current_user(authorization, session_token)
    
    # Get origin from request
    origin = str(request.base_url).rstrip('/')
    
    # Create success and cancel URLs
    success_url = f"{origin}/order-success?session_id={{CHECKOUT_SESSION_ID}}"
    cancel_url = f"{origin}/cart"
    
    # Initialize Stripe checkout
    webhook_url = f"{origin}/api/webhook/stripe"
    stripe_checkout = StripeCheckout(
        api_key=os.environ.get("STRIPE_API_KEY"),
        webhook_url=webhook_url
    )
    
    # Create checkout session
    checkout_request = CheckoutSessionRequest(
        amount=float(amount),
        currency="usd",
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={
            "user_id": user.user_id,
            "order_id": order_id
        }
    )
    
    session_response: CheckoutSessionResponse = await stripe_checkout.create_checkout_session(checkout_request)
    
    # Create payment transaction record
    transaction = PaymentTransaction(
        session_id=session_response.session_id,
        user_id=user.user_id,
        amount=amount,
        currency="usd",
        metadata={"order_id": order_id}
    )
    
    await db.payment_transactions.insert_one(transaction.model_dump())
    
    return {
        "url": session_response.url,
        "session_id": session_response.session_id
    }

@api_router.get("/payments/status/{session_id}")
async def get_payment_status(session_id: str):
    """Get payment status"""
    # Get transaction from DB
    transaction = await db.payment_transactions.find_one({"session_id": session_id}, {"_id": 0})
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    # If already processed, return cached status
    if transaction["payment_status"] == "paid":
        return transaction
    
    # Check with Stripe
    stripe_checkout = StripeCheckout(
        api_key=os.environ.get("STRIPE_API_KEY"),
        webhook_url=""
    )
    
    status_response: CheckoutStatusResponse = await stripe_checkout.get_checkout_status(session_id)
    
    # Update transaction if status changed
    if status_response.payment_status == "paid" and transaction["payment_status"] != "paid":
        await db.payment_transactions.update_one(
            {"session_id": session_id},
            {
                "$set": {
                    "status": "completed",
                    "payment_status": status_response.payment_status,
                    "updated_at": datetime.now(timezone.utc)
                }
            }
        )
        
        # Update order status if paid
        if transaction.get("metadata", {}).get("order_id"):
            await db.orders.update_one(
                {"order_id": transaction["metadata"]["order_id"]},
                {
                    "$set": {
                        "status": "confirmed",
                        "updated_at": datetime.now(timezone.utc)
                    }
                }
            )
    
    return {
        "session_id": session_id,
        "status": status_response.status,
        "payment_status": status_response.payment_status,
        "amount": status_response.amount_total / 100,
        "currency": status_response.currency
    }

@api_router.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    """Handle Stripe webhooks"""
    body = await request.body()
    signature = request.headers.get("Stripe-Signature")
    
    stripe_checkout = StripeCheckout(
        api_key=os.environ.get("STRIPE_API_KEY"),
        webhook_url=""
    )
    
    try:
        webhook_response = await stripe_checkout.handle_webhook(body, signature)
        
        # Update transaction based on webhook event
        if webhook_response.payment_status == "paid":
            await db.payment_transactions.update_one(
                {"session_id": webhook_response.session_id},
                {
                    "$set": {
                        "status": "completed",
                        "payment_status": "paid",
                        "updated_at": datetime.now(timezone.utc)
                    }
                }
            )
        
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# ==================== REVIEW ENDPOINTS ====================

@api_router.post("/reviews")
async def create_review(
    data: CreateReview,
    authorization: Optional[str] = Header(None),
    session_token: Optional[str] = Cookie(None)
):
    """Create a review"""
    user = await get_current_user(authorization, session_token)
    
    review = Review(
        user_id=user.user_id,
        user_name=user.name,
        restaurant_id=data.restaurant_id,
        order_id=data.order_id,
        rating=data.rating,
        comment=data.comment
    )
    
    await db.reviews.insert_one(review.model_dump())
    
    # Update restaurant rating (simple average)
    reviews = await db.reviews.find({"restaurant_id": data.restaurant_id}).to_list(1000)
    avg_rating = sum(r["rating"] for r in reviews) / len(reviews)
    
    await db.restaurants.update_one(
        {"restaurant_id": data.restaurant_id},
        {"$set": {"rating": round(avg_rating, 1)}}
    )
    
    return review.model_dump()

# ==================== PROFILE ENDPOINTS ====================

@api_router.get("/profile")
async def get_profile(
    authorization: Optional[str] = Header(None),
    session_token: Optional[str] = Cookie(None)
):
    """Get user profile"""
    user = await get_current_user(authorization, session_token)
    user_dict = user.model_dump()
    user_dict.pop('password_hash', None)
    
    # Get order count
    order_count = await db.orders.count_documents({"user_id": user.user_id})
    user_dict["order_count"] = order_count
    
    return user_dict

@api_router.put("/profile")
async def update_profile(
    data: Dict[str, Any],
    authorization: Optional[str] = Header(None),
    session_token: Optional[str] = Cookie(None)
):
    """Update user profile"""
    user = await get_current_user(authorization, session_token)
    
    # Remove fields that shouldn't be updated
    data.pop('user_id', None)
    data.pop('password_hash', None)
    data.pop('email', None)
    data.pop('created_at', None)
    
    await db.users.update_one(
        {"user_id": user.user_id},
        {"$set": data}
    )
    
    return {"message": "Profile updated"}

@api_router.post("/profile/addresses")
async def add_address(
    address: Dict[str, Any],
    authorization: Optional[str] = Header(None),
    session_token: Optional[str] = Cookie(None)
):
    """Add delivery address"""
    user = await get_current_user(authorization, session_token)
    
    address["id"] = f"addr_{uuid.uuid4().hex[:8]}"
    
    await db.users.update_one(
        {"user_id": user.user_id},
        {"$push": {"addresses": address}}
    )
    
    return address

# ==================== SEED DATA ====================

@api_router.get("/seed-data")
async def seed_data():
    """Seed database with sample restaurants and menus"""
    # Check if already seeded
    count = await db.restaurants.count_documents({})
    if count > 0:
        return {"message": "Database already seeded", "restaurant_count": count}
    
    # Sample restaurants with high-quality images
    restaurants_data = [
        {
            "name": "Sakura Sushi House",
            "description": "Authentic Japanese sushi and sashimi prepared by master chefs",
            "image": "https://images.unsplash.com/photo-1605490499457-277af25da705",
            "cuisine_type": "Japanese",
            "rating": 4.8,
            "delivery_time": "25-35 min",
            "price_range": "$$$",
            "location": {"lat": 37.7749, "lng": -122.4194, "address": "123 Sushi St"},
            "featured": True,
            "menu_categories": ["Sushi Rolls", "Sashimi", "Appetizers", "Drinks"]
        },
        {
            "name": "The Gourmet Burger Co.",
            "description": "Premium handcrafted burgers with artisanal ingredients",
            "image": "https://images.unsplash.com/photo-1593022754339-f23454332fd8",
            "cuisine_type": "American",
            "rating": 4.6,
            "delivery_time": "20-30 min",
            "price_range": "$$",
            "location": {"lat": 37.7750, "lng": -122.4195, "address": "456 Burger Ave"},
            "featured": True,
            "menu_categories": ["Burgers", "Sides", "Shakes", "Salads"]
        },
        {
            "name": "Fresh & Green",
            "description": "Healthy bowls, salads, and smoothies made with organic ingredients",
            "image": "https://images.unsplash.com/photo-1662714208483-3480ccd2de39",
            "cuisine_type": "Healthy",
            "rating": 4.7,
            "delivery_time": "15-25 min",
            "price_range": "$$",
            "location": {"lat": 37.7751, "lng": -122.4196, "address": "789 Green Way"},
            "featured": True,
            "menu_categories": ["Power Bowls", "Salads", "Smoothies", "Juices"]
        },
        {
            "name": "Bella Italia",
            "description": "Traditional Italian pasta and pizza from family recipes",
            "image": "https://images.unsplash.com/photo-1616671276441-2f2c277b8bf9",
            "cuisine_type": "Italian",
            "rating": 4.5,
            "delivery_time": "30-40 min",
            "price_range": "$$",
            "location": {"lat": 37.7752, "lng": -122.4197, "address": "321 Italia Rd"},
            "featured": False,
            "menu_categories": ["Pasta", "Pizza", "Appetizers", "Desserts"]
        },
        {
            "name": "Taco Fiesta",
            "description": "Authentic Mexican street food and tacos",
            "image": "https://images.unsplash.com/photo-1599021277840-9d3f4f383742",
            "cuisine_type": "Mexican",
            "rating": 4.4,
            "delivery_time": "20-30 min",
            "price_range": "$",
            "location": {"lat": 37.7753, "lng": -122.4198, "address": "555 Taco Ln"},
            "featured": False,
            "menu_categories": ["Tacos", "Burritos", "Quesadillas", "Sides"]
        },
        {
            "name": "Sweet Treats Bakery",
            "description": "Artisanal cakes, pastries, and desserts baked fresh daily",
            "image": "https://images.unsplash.com/photo-1589218436045-ee320057f443",
            "cuisine_type": "Desserts",
            "rating": 4.9,
            "delivery_time": "25-35 min",
            "price_range": "$$",
            "location": {"lat": 37.7754, "lng": -122.4199, "address": "888 Sweet St"},
            "featured": True,
            "menu_categories": ["Cakes", "Pastries", "Cookies", "Ice Cream"]
        },
        {
            "name": "Dragon Wok",
            "description": "Szechuan and Cantonese cuisine with bold flavors",
            "image": "https://images.unsplash.com/photo-1583245537385-e7ba78378183",
            "cuisine_type": "Chinese",
            "rating": 4.3,
            "delivery_time": "25-35 min",
            "price_range": "$$",
            "location": {"lat": 37.7755, "lng": -122.4200, "address": "999 Dragon Dr"},
            "featured": False,
            "menu_categories": ["Noodles", "Rice Dishes", "Stir Fry", "Dim Sum"]
        },
        {
            "name": "The Steakhouse",
            "description": "Premium cuts of steak and classic American fare",
            "image": "https://images.unsplash.com/photo-1580302499247-b933c03eaca9",
            "cuisine_type": "Steakhouse",
            "rating": 4.7,
            "delivery_time": "35-45 min",
            "price_range": "$$$$",
            "location": {"lat": 37.7756, "lng": -122.4201, "address": "111 Steak Ave"},
            "featured": True,
            "menu_categories": ["Steaks", "Seafood", "Sides", "Salads"]
        },
        {
            "name": "Pho Paradise",
            "description": "Traditional Vietnamese pho and banh mi",
            "image": "https://images.unsplash.com/photo-1552526881-721ce8509abb",
            "cuisine_type": "Vietnamese",
            "rating": 4.6,
            "delivery_time": "20-30 min",
            "price_range": "$",
            "location": {"lat": 37.7757, "lng": -122.4202, "address": "222 Pho Rd"},
            "featured": False,
            "menu_categories": ["Pho", "Banh Mi", "Spring Rolls", "Rice Dishes"]
        },
        {
            "name": "Mediterranean Mezze",
            "description": "Fresh Mediterranean cuisine with vibrant flavors",
            "image": "https://images.unsplash.com/photo-1564759298141-cef86f51d4d4",
            "cuisine_type": "Mediterranean",
            "rating": 4.5,
            "delivery_time": "25-35 min",
            "price_range": "$$",
            "location": {"lat": 37.7758, "lng": -122.4203, "address": "333 Med Way"},
            "featured": False,
            "menu_categories": ["Mezze", "Kebabs", "Salads", "Wraps"]
        },
        {
            "name": "Breakfast Club",
            "description": "All-day breakfast favorites and brunch classics",
            "image": "https://images.unsplash.com/photo-1565004602745-718e1b0d44f8",
            "cuisine_type": "Breakfast",
            "rating": 4.4,
            "delivery_time": "15-25 min",
            "price_range": "$$",
            "location": {"lat": 37.7759, "lng": -122.4204, "address": "444 Breakfast Blvd"},
            "featured": False,
            "menu_categories": ["Pancakes", "Eggs", "Sandwiches", "Coffee"]
        },
        {
            "name": "Curry Kingdom",
            "description": "Authentic Indian curries and tandoori specialties",
            "image": "https://images.unsplash.com/photo-1607103071568-159bb70b4bf0",
            "cuisine_type": "Indian",
            "rating": 4.6,
            "delivery_time": "30-40 min",
            "price_range": "$$",
            "location": {"lat": 37.7760, "lng": -122.4205, "address": "555 Curry Ct"},
            "featured": False,
            "menu_categories": ["Curries", "Tandoori", "Biryani", "Naan"]
        },
        {
            "name": "The Smoothie Bar",
            "description": "Fresh smoothies, acai bowls, and healthy snacks",
            "image": "https://images.unsplash.com/photo-1662714208483-3480ccd2de39",
            "cuisine_type": "Smoothies",
            "rating": 4.5,
            "delivery_time": "10-20 min",
            "price_range": "$",
            "location": {"lat": 37.7761, "lng": -122.4206, "address": "666 Smoothie St"},
            "featured": False,
            "menu_categories": ["Smoothies", "Acai Bowls", "Juices", "Snacks"]
        },
        {
            "name": "BBQ Pit Stop",
            "description": "Slow-smoked BBQ ribs, brisket, and pulled pork",
            "image": "https://images.unsplash.com/photo-1599021277840-9d3f4f383742",
            "cuisine_type": "BBQ",
            "rating": 4.7,
            "delivery_time": "30-40 min",
            "price_range": "$$",
            "location": {"lat": 37.7762, "lng": -122.4207, "address": "777 BBQ Blvd"},
            "featured": False,
            "menu_categories": ["Ribs", "Brisket", "Pulled Pork", "Sides"]
        },
        {
            "name": "Artisan Bread Co.",
            "description": "Handcrafted breads, sandwiches, and soups",
            "image": "https://images.unsplash.com/photo-1579711220373-155ffc441b36",
            "cuisine_type": "Bakery",
            "rating": 4.8,
            "delivery_time": "20-30 min",
            "price_range": "$$",
            "location": {"lat": 37.7763, "lng": -122.4208, "address": "888 Bread Ave"},
            "featured": True,
            "menu_categories": ["Sandwiches", "Soups", "Breads", "Pastries"]
        }
    ]
    
    # Insert restaurants and create menus
    for rest_data in restaurants_data:
        restaurant = Restaurant(**rest_data)
        await db.restaurants.insert_one(restaurant.model_dump())
        
        # Create sample menu items for each restaurant
        menu_items = []
        
        if restaurant.cuisine_type == "Japanese":
            menu_items = [
                {"name": "California Roll", "description": "Crab, avocado, cucumber", "price": 12.99, "category": "Sushi Rolls", "image": "https://images.unsplash.com/photo-1605490499457-277af25da705"},
                {"name": "Spicy Tuna Roll", "description": "Tuna, spicy mayo, cucumber", "price": 14.99, "category": "Sushi Rolls", "image": "https://images.unsplash.com/photo-1583245537385-e7ba78378183"},
                {"name": "Salmon Sashimi", "description": "Fresh salmon slices", "price": 16.99, "category": "Sashimi", "image": "https://images.unsplash.com/photo-1605490499457-277af25da705"},
                {"name": "Edamame", "description": "Steamed soybeans with sea salt", "price": 5.99, "category": "Appetizers", "image": "https://images.unsplash.com/photo-1583245537385-e7ba78378183"},
            ]
        elif restaurant.cuisine_type == "American":
            menu_items = [
                {"name": "Classic Cheeseburger", "description": "Angus beef, cheddar, lettuce, tomato", "price": 13.99, "category": "Burgers", "image": "https://images.unsplash.com/photo-1593022754339-f23454332fd8"},
                {"name": "Bacon Burger", "description": "Double bacon, BBQ sauce, onion rings", "price": 15.99, "category": "Burgers", "image": "https://images.unsplash.com/photo-1552526881-721ce8509abb"},
                {"name": "Truffle Fries", "description": "Hand-cut fries with truffle oil", "price": 7.99, "category": "Sides", "image": "https://images.unsplash.com/photo-1599021277840-9d3f4f383742"},
                {"name": "Chocolate Shake", "description": "Rich chocolate milkshake", "price": 6.99, "category": "Shakes", "image": "https://images.unsplash.com/photo-1565004602745-718e1b0d44f8"},
            ]
        elif restaurant.cuisine_type == "Healthy":
            menu_items = [
                {"name": "Power Bowl", "description": "Quinoa, grilled chicken, avocado, veggies", "price": 14.99, "category": "Power Bowls", "image": "https://images.unsplash.com/photo-1662714208483-3480ccd2de39"},
                {"name": "Green Goddess Salad", "description": "Mixed greens, cucumber, feta, herbs", "price": 12.99, "category": "Salads", "image": "https://images.unsplash.com/photo-1662714208483-3480ccd2de39"},
                {"name": "Berry Blast Smoothie", "description": "Mixed berries, banana, almond milk", "price": 8.99, "category": "Smoothies", "image": "https://images.unsplash.com/photo-1565004602745-718e1b0d44f8"},
                {"name": "Green Juice", "description": "Kale, cucumber, apple, lemon", "price": 7.99, "category": "Juices", "image": "https://images.unsplash.com/photo-1662714208483-3480ccd2de39"},
            ]
        else:
            # Generic items for other cuisines
            menu_items = [
                {"name": f"Signature Dish", "description": f"Our most popular {restaurant.cuisine_type} dish", "price": 15.99, "category": restaurant.menu_categories[0], "image": restaurant.image},
                {"name": f"Special Combo", "description": f"A delicious {restaurant.cuisine_type} combination", "price": 18.99, "category": restaurant.menu_categories[0], "image": restaurant.image},
                {"name": f"Appetizer Platter", "description": f"Assorted {restaurant.cuisine_type} appetizers", "price": 12.99, "category": restaurant.menu_categories[1] if len(restaurant.menu_categories) > 1 else restaurant.menu_categories[0], "image": restaurant.image},
            ]
        
        for item_data in menu_items:
            menu_item = MenuItem(
                restaurant_id=restaurant.restaurant_id,
                **item_data,
                dietary_tags=[]
            )
            await db.menu_items.insert_one(menu_item.model_dump())
    
    return {"message": "Database seeded successfully", "restaurant_count": len(restaurants_data)}

# Include the router in the main app
fastapi_app.include_router(api_router)

# Serve screenshots for download
fastapi_app.mount("/api/screenshots", StaticFiles(directory="/app/backend/static/screenshots"), name="screenshots")

@fastapi_app.get("/api/download-screenshots")
async def download_screenshots_page():
    """Page to download all App Store screenshots"""
    import os
    files = sorted([f for f in os.listdir("/app/backend/static/screenshots") if f.endswith('.png')])
    links = "".join(f'<a href="/api/screenshots/{f}" download="{f}" style="display:block;margin:12px 0;padding:14px 20px;background:#87A96B;color:white;border-radius:10px;text-decoration:none;font-weight:600;text-align:center">{f} (1284x2778px)</a>' for f in files)
    return HTMLResponse(f"""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>body{{font-family:system-ui;max-width:500px;margin:40px auto;padding:20px;background:#F0F2ED}}h1{{color:#333}}p{{color:#666}}</style></head>
    <body><h1>App Store Screenshots</h1><p>Click each to download (all 1284x2778px):</p>{links}
    <p style="margin-top:30px;font-size:13px;color:#999">Right-click → Save As if clicking doesn't download</p></body></html>
    """)

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@fastapi_app.on_event("startup")
async def startup():
    logger.info("Server starting...")

@fastapi_app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
    logger.info("Server shutting down...")

# Wrap FastAPI with Socket.IO
socket_app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app, socketio_path='/api/socket.io')
app = socket_app

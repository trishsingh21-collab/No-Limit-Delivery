from fastapi import FastAPI, APIRouter, HTTPException, Request, Header, Response, Cookie
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
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
from supabase import create_client, Client

load_dotenv()

# ==================== LOGGING ====================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("server")

# ==================== SUPABASE CLIENT ====================
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://gxotqmfripuffxnanrfi.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==================== SOCKETIO ====================
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

# ==================== FASTAPI APP ====================
fastapi_app = FastAPI()
api_router = APIRouter(prefix="/api")

# ==================== MODELS ====================
class User(BaseModel):
    user_id: str = Field(default_factory=lambda: f"user_{uuid.uuid4().hex[:12]}")
    email: str
    password_hash: str
    name: str = ""
    phone: str = ""
    addresses: List[Dict[str, Any]] = []
    loyalty_points: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class OrderItem(BaseModel):
    item_id: str = ""
    name: str
    price: float
    quantity: int = 1

class Order(BaseModel):
    order_id: str = Field(default_factory=lambda: f"order_{uuid.uuid4().hex[:12]}")
    user_id: str
    restaurant_id: str
    restaurant_name: str
    items: List[OrderItem]
    subtotal: float
    delivery_fee: float = 30.0
    tax: float
    total: float
    delivery_address: Dict[str, Any]
    payment_method: str = "cash"
    order_notes: str = ""
    allergies: List[str] = []
    tip: float = 0
    promo_code: Optional[str] = None
    status: str = "pending"
    payment_status: str = "unpaid"
    pf_payment_id: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    estimated_delivery: Optional[datetime] = None

class CreateOrder(BaseModel):
    restaurant_id: str
    items: List[OrderItem]
    delivery_address: Dict[str, Any]
    payment_method: str = "cash"
    order_notes: str = ""
    allergies: List[str] = []
    tip: float = 0
    promo_code: Optional[str] = None

class SignupRequest(BaseModel):
    email: str
    password: str
    name: str = ""

class LoginRequest(BaseModel):
    email: str
    password: str

class AIRecommendationRequest(BaseModel):
    preferences: str = ""
    mood: str = ""

class MoodSuggestionRequest(BaseModel):
    mood: str

class PaymentTransaction(BaseModel):
    transaction_id: str = Field(default_factory=lambda: f"txn_{uuid.uuid4().hex[:12]}")
    session_id: str = ""
    user_id: str
    amount: float
    currency: str = "ZAR"
    payment_status: str = "pending"
    metadata: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# ==================== HELPERS ====================
sessions = {}

async def get_current_user(authorization: Optional[str] = None, session_token: Optional[str] = None):
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
    elif session_token:
        token = session_token
    if not token or token not in sessions:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user_id = sessions[token]
    result = supabase.table("users").select("*").eq("user_id", user_id).execute()
    if not result.data:
        raise HTTPException(status_code=401, detail="User not found")
    user_data = result.data[0]
    return User(**user_data)

# ==================== AUTH ENDPOINTS ====================
@api_router.post("/auth/signup")
async def signup(data: SignupRequest):
    existing = supabase.table("users").select("user_id").eq("email", data.email).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    password_hash = bcrypt.hashpw(data.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user = User(email=data.email, password_hash=password_hash, name=data.name)
    
    supabase.table("users").insert({
        "user_id": user.user_id, "email": user.email, "password_hash": user.password_hash,
        "name": user.name, "phone": "", "addresses": [], "loyalty_points": 0
    }).execute()
    
    session_token = f"session_{uuid.uuid4().hex}"
    sessions[session_token] = user.user_id
    
    return {"user": {"user_id": user.user_id, "email": user.email, "name": user.name}, "session_token": session_token}

@api_router.post("/auth/login")
async def login(data: LoginRequest):
    result = supabase.table("users").select("*").eq("email", data.email).execute()
    if not result.data:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user_data = result.data[0]
    if not bcrypt.checkpw(data.password.encode('utf-8'), user_data["password_hash"].encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    session_token = f"session_{uuid.uuid4().hex}"
    sessions[session_token] = user_data["user_id"]
    
    return {
        "user": {"user_id": user_data["user_id"], "email": user_data["email"], "name": user_data["name"], "phone": user_data.get("phone", ""), "loyalty_points": user_data.get("loyalty_points", 0)},
        "session_token": session_token
    }

@api_router.get("/auth/me")
async def get_me(authorization: Optional[str] = Header(None), session_token: Optional[str] = Cookie(None)):
    user = await get_current_user(authorization, session_token)
    return {"user_id": user.user_id, "email": user.email, "name": user.name, "phone": user.phone, "loyalty_points": user.loyalty_points}

@api_router.post("/auth/logout")
async def logout(authorization: Optional[str] = Header(None), session_token: Optional[str] = Cookie(None)):
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
    elif session_token:
        token = session_token
    if token and token in sessions:
        del sessions[token]
    return {"message": "Logged out"}

# ==================== SERVICES ====================
@api_router.get("/services")
async def get_services():
    result = supabase.table("services").select("*").eq("active", True).execute()
    return result.data

# ==================== RESTAURANTS ====================
@api_router.get("/restaurants")
async def get_restaurants(service_type: Optional[str] = None, featured: Optional[bool] = None):
    query = supabase.table("restaurants").select("*").eq("active", True)
    if service_type:
        query = query.eq("service_type", service_type)
    if featured is not None:
        query = query.eq("featured", featured)
    result = query.execute()
    return result.data

@api_router.get("/restaurants/{restaurant_id}")
async def get_restaurant(restaurant_id: str):
    result = supabase.table("restaurants").select("*").eq("restaurant_id", restaurant_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return result.data[0]

@api_router.get("/restaurants/{restaurant_id}/menu")
async def get_menu(restaurant_id: str, category: Optional[str] = None):
    query = supabase.table("menu_items").select("*").eq("restaurant_id", restaurant_id).eq("available", True)
    if category:
        query = query.eq("category", category)
    result = query.execute()
    return result.data

@api_router.get("/restaurants/{restaurant_id}/reviews")
async def get_reviews(restaurant_id: str):
    result = supabase.table("reviews").select("*").eq("restaurant_id", restaurant_id).order("created_at", desc=True).limit(20).execute()
    return result.data

# ==================== ORDERS ====================
@api_router.post("/orders")
async def create_order(data: CreateOrder, authorization: Optional[str] = Header(None), session_token: Optional[str] = Cookie(None)):
    user = await get_current_user(authorization, session_token)
    
    rest_result = supabase.table("restaurants").select("name").eq("restaurant_id", data.restaurant_id).execute()
    restaurant_name = rest_result.data[0]["name"] if rest_result.data else "Unknown"
    
    subtotal = sum(item.price * item.quantity for item in data.items)
    delivery_fee = 30.0
    tax = subtotal * 0.15
    total = subtotal + delivery_fee + tax + data.tip
    
    order = Order(
        user_id=user.user_id, restaurant_id=data.restaurant_id, restaurant_name=restaurant_name,
        items=[item.model_dump() for item in data.items], subtotal=round(subtotal, 2),
        delivery_fee=round(delivery_fee, 2), tax=round(tax, 2), total=round(total, 2),
        delivery_address=data.delivery_address, payment_method=data.payment_method,
        order_notes=data.order_notes, allergies=data.allergies, tip=data.tip,
        promo_code=data.promo_code, estimated_delivery=datetime.now(timezone.utc) + timedelta(minutes=40)
    )
    
    order_dict = order.model_dump()
    order_dict["created_at"] = order_dict["created_at"].isoformat()
    order_dict["updated_at"] = order_dict["updated_at"].isoformat()
    order_dict["estimated_delivery"] = order_dict["estimated_delivery"].isoformat() if order_dict["estimated_delivery"] else None
    # Remove fields not in schema
    order_dict.pop("id", None)
    
    supabase.table("orders").insert(order_dict).execute()
    
    # Update loyalty points
    supabase.table("users").update({"loyalty_points": user.loyalty_points + 10}).eq("user_id", user.user_id).execute()
    
    return order.model_dump()

@api_router.get("/orders")
async def get_orders(authorization: Optional[str] = Header(None), session_token: Optional[str] = Cookie(None)):
    user = await get_current_user(authorization, session_token)
    result = supabase.table("orders").select("*").eq("user_id", user.user_id).order("created_at", desc=True).execute()
    return result.data

@api_router.get("/orders/{order_id}")
async def get_order(order_id: str, authorization: Optional[str] = Header(None), session_token: Optional[str] = Cookie(None)):
    user = await get_current_user(authorization, session_token)
    result = supabase.table("orders").select("*").eq("order_id", order_id).eq("user_id", user.user_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Order not found")
    return result.data[0]

@api_router.put("/orders/{order_id}/status")
async def update_order_status(order_id: str, request: Request):
    body = await request.json()
    status = body.get("status")
    supabase.table("orders").update({"status": status, "updated_at": datetime.now(timezone.utc).isoformat()}).eq("order_id", order_id).execute()
    return {"message": "Order status updated", "status": status}

# ==================== PROFILE ====================
@api_router.get("/profile")
async def get_profile(authorization: Optional[str] = Header(None), session_token: Optional[str] = Cookie(None)):
    user = await get_current_user(authorization, session_token)
    orders_result = supabase.table("orders").select("order_id").eq("user_id", user.user_id).execute()
    return {
        "user_id": user.user_id, "email": user.email, "name": user.name, "phone": user.phone,
        "loyalty_points": user.loyalty_points, "total_orders": len(orders_result.data),
        "addresses": user.addresses
    }

@api_router.put("/profile")
async def update_profile(request: Request, authorization: Optional[str] = Header(None), session_token: Optional[str] = Cookie(None)):
    user = await get_current_user(authorization, session_token)
    body = await request.json()
    update_data = {}
    if "name" in body: update_data["name"] = body["name"]
    if "phone" in body: update_data["phone"] = body["phone"]
    if update_data:
        supabase.table("users").update(update_data).eq("user_id", user.user_id).execute()
    return {"message": "Profile updated"}

# ==================== PAYFAST PAYMENT ====================
PAYFAST_CHECKOUT_FIELD_ORDER = [
    "merchant_id", "merchant_key", "return_url", "cancel_url", "notify_url",
    "name_first", "name_last", "email_address", "cell_number",
    "m_payment_id", "amount", "item_name", "item_description",
]

def get_payfast_config():
    return {
        "merchant_id": os.getenv("PAYFAST_MERCHANT_ID", "12038995"),
        "merchant_key": os.getenv("PAYFAST_MERCHANT_KEY", "fchs0cmm3oufn"),
        "passphrase": os.getenv("PAYFAST_PASSPHRASE", ""),
        "sandbox": os.getenv("PAYFAST_SANDBOX", "false").lower() == "true",
    }

def calculate_payfast_signature(data: dict, passphrase: str) -> str:
    filtered = {k: str(v).strip() for k, v in data.items() if k != 'signature' and v is not None and str(v).strip()}
    priority_dict = {k: i for i, k in enumerate(PAYFAST_CHECKOUT_FIELD_ORDER)}
    sorted_keys = sorted(filtered.keys(), key=lambda k: priority_dict.get(k, 999))
    param_str = '&'.join(f"{key}={urllib.parse.quote_plus(filtered[key])}" for key in sorted_keys)
    if passphrase:
        param_str += f"&passphrase={urllib.parse.quote_plus(passphrase)}"
    return md5(param_str.encode('utf-8')).hexdigest()

@api_router.post("/payments/payfast/create")
async def create_payfast_payment(request: Request, authorization: Optional[str] = Header(None), session_token: Optional[str] = Cookie(None)):
    user = await get_current_user(authorization, session_token)
    body = await request.json()
    order_id = body.get("order_id")
    if not order_id:
        raise HTTPException(status_code=400, detail="order_id required")
    
    order_result = supabase.table("orders").select("*").eq("order_id", order_id).eq("user_id", user.user_id).execute()
    if not order_result.data:
        raise HTTPException(status_code=404, detail="Order not found")
    order = order_result.data[0]
    
    pf = get_payfast_config()
    base_url = str(request.base_url).rstrip('/')
    
    payment_data = {
        "merchant_id": pf["merchant_id"], "merchant_key": pf["merchant_key"],
        "return_url": f"{base_url}/api/payments/payfast/return?order_id={order_id}",
        "cancel_url": f"{base_url}/api/payments/payfast/cancel?order_id={order_id}",
        "notify_url": f"{base_url}/api/payments/payfast/notify",
        "name_first": user.name.split()[0] if user.name else "Customer",
        "email_address": user.email, "m_payment_id": order_id,
        "amount": f"{order['total']:.2f}",
        "item_name": f"No Limit Delivery - Order {order_id[:16]}",
    }
    payment_data["signature"] = calculate_payfast_signature(payment_data, pf["passphrase"])
    payfast_url = "https://sandbox.payfast.co.za/eng/process" if pf["sandbox"] else "https://www.payfast.co.za/eng/process"
    
    supabase.table("orders").update({"status": "awaiting_payment", "payment_method": "payfast"}).eq("order_id", order_id).execute()
    
    return {"payfast_url": payfast_url, "payment_data": payment_data, "order_id": order_id, "sandbox": pf["sandbox"]}

@api_router.post("/payments/payfast/notify")
async def payfast_itn(request: Request):
    try:
        form_data = await request.form()
        data = dict(form_data)
        order_id = data.get("m_payment_id", "")
        payment_status = data.get("payment_status", "")
        
        if payment_status == "COMPLETE":
            supabase.table("orders").update({"status": "confirmed", "payment_status": "paid", "pf_payment_id": data.get("pf_payment_id", ""), "updated_at": datetime.now(timezone.utc).isoformat()}).eq("order_id", order_id).execute()
        elif payment_status == "CANCELLED":
            supabase.table("orders").update({"status": "cancelled", "payment_status": "cancelled"}).eq("order_id", order_id).execute()
        return Response(status_code=200, content="OK")
    except Exception as e:
        logger.error(f"PayFast ITN error: {e}")
        return Response(status_code=200, content="OK")

@api_router.get("/payments/payfast/return")
async def payfast_return(order_id: str = ""):
    if order_id:
        supabase.table("orders").update({"status": "confirmed", "payment_status": "paid", "updated_at": datetime.now(timezone.utc).isoformat()}).eq("order_id", order_id).execute()
    return HTMLResponse(f'<html><body style="font-family:system-ui;display:flex;justify-content:center;align-items:center;min-height:100vh;background:#F0F2ED;text-align:center"><div style="padding:40px;background:white;border-radius:16px;max-width:360px"><h2>Payment Successful!</h2><p>Your order has been confirmed.</p><a href="/" style="display:inline-block;margin-top:20px;padding:14px 28px;background:#87A96B;color:white;border-radius:12px;text-decoration:none">Back to App</a></div></body></html>')

@api_router.get("/payments/payfast/cancel")
async def payfast_cancel(order_id: str = ""):
    if order_id:
        supabase.table("orders").update({"status": "payment_cancelled"}).eq("order_id", order_id).execute()
    return HTMLResponse(f'<html><body style="font-family:system-ui;display:flex;justify-content:center;align-items:center;min-height:100vh;background:#F0F2ED;text-align:center"><div style="padding:40px;background:white;border-radius:16px;max-width:360px"><h2>Payment Cancelled</h2><p>Your payment was not completed.</p><a href="/" style="display:inline-block;margin-top:20px;padding:14px 28px;background:#87A96B;color:white;border-radius:12px;text-decoration:none">Back to App</a></div></body></html>')

# ==================== AI FEATURES (FALLBACK) ====================
@api_router.post("/ai/recommendations")
async def get_recommendations(data: AIRecommendationRequest, authorization: Optional[str] = Header(None), session_token: Optional[str] = Cookie(None)):
    user = await get_current_user(authorization, session_token)
    result = supabase.table("restaurants").select("*").eq("active", True).limit(5).execute()
    return {"recommendations": "Check out our featured restaurants!", "restaurants": result.data}

@api_router.post("/ai/randomizer")
async def food_randomizer():
    import random
    result = supabase.table("restaurants").select("*").eq("active", True).execute()
    if result.data:
        pick = random.choice(result.data)
        return {"suggestion": f"Today's pick: {pick['name']}! Great {pick.get('cuisine_type', 'food')} awaits.", "restaurants": result.data[:5]}
    return {"suggestion": "Browse our providers!", "restaurants": []}

@api_router.post("/ai/mood-suggestions")
async def mood_suggestions(data: MoodSuggestionRequest):
    result = supabase.table("restaurants").select("*").eq("active", True).limit(5).execute()
    return {"suggestions": f"Based on your {data.mood} mood, try these!", "restaurants": result.data}

# ==================== REVIEWS ====================
@api_router.post("/restaurants/{restaurant_id}/reviews")
async def create_review(restaurant_id: str, request: Request, authorization: Optional[str] = Header(None), session_token: Optional[str] = Cookie(None)):
    user = await get_current_user(authorization, session_token)
    body = await request.json()
    review = {"review_id": f"rev_{uuid.uuid4().hex[:12]}", "user_id": user.user_id, "restaurant_id": restaurant_id, "rating": body.get("rating", 5), "comment": body.get("comment", "")}
    supabase.table("reviews").insert(review).execute()
    return review

# ==================== SOCKET.IO ====================
@sio.event
async def connect(sid, environ):
    logger.info(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    logger.info(f"Client disconnected: {sid}")

@sio.event
async def track_order(sid, data):
    order_id = data.get("order_id")
    if order_id:
        await sio.enter_room(sid, f"order_{order_id}")

# ==================== STARTUP/SHUTDOWN ====================
@fastapi_app.on_event("startup")
async def startup():
    logger.info("Server starting...")

@fastapi_app.on_event("shutdown")
async def shutdown():
    logger.info("Server shutting down...")

# ==================== REGISTER ROUTER & CORS ====================
fastapi_app.include_router(api_router)

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== SOCKET WRAP ====================
socket_app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app, socketio_path='/api/socket.io')
app = socket_app

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

# ==================== LOAD ENV ====================
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# ==================== LOGGING ====================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== DATABASE ====================
mongo_url = os.environ.get("MONGO_URL", "")
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get("DB_NAME", "test")]

# ==================== SOCKET ====================
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

# ✅ FIXED HERE
fastapi_app = FastAPI(
    root_path="/proxy/8000"
)

api_router = APIRouter(prefix="/api")

# ==================== MODELS ====================
class User(BaseModel):
    user_id: str = Field(default_factory=lambda: f"user_{uuid.uuid4().hex[:12]}")
    email: str
    name: str
    password_hash: Optional[str] = None

class UserSignup(BaseModel):
    email: str
    password: str
    name: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserSession(BaseModel):
    session_token: str = Field(default_factory=lambda: f"session_{uuid.uuid4().hex}")
    user_id: str
    expires_at: datetime

# ==================== AUTH HELPERS ====================
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

async def get_current_user(authorization: Optional[str] = None):
    if not authorization:
        raise HTTPException(status_code=401, detail="No token")

    token = authorization.replace("Bearer ", "")
    session = await db.user_sessions.find_one({"session_token": token})

    if not session:
        raise HTTPException(status_code=401, detail="Invalid session")

    user = await db.users.find_one({"user_id": session["user_id"]})
    return user

# ==================== AUTH ROUTES ====================
@api_router.post("/auth/signup")
async def signup(data: UserSignup):
    existing = await db.users.find_one({"email": data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email exists")

    user = User(
        email=data.email,
        name=data.name,
        password_hash=hash_password(data.password)
    )

    await db.users.insert_one(user.model_dump())

    session = UserSession(
        user_id=user.user_id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=7)
    )

    await db.user_sessions.insert_one(session.model_dump())

    user_dict = user.model_dump()
    user_dict.pop("password_hash")

    return {
        "user": user_dict,
        "session_token": session.session_token
    }

@api_router.post("/auth/login")
async def login(data: UserLogin):
    user = await db.users.find_one({"email": data.email})

    if not user or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    session = UserSession(
        user_id=user["user_id"],
        expires_at=datetime.now(timezone.utc) + timedelta(days=7)
    )

    await db.user_sessions.insert_one(session.model_dump())

    user.pop("password_hash")

    return {
        "user": user,
        "session_token": session.session_token
    }

@api_router.get("/auth/me")
async def get_me(authorization: Optional[str] = Header(None)):
    user = await get_current_user(authorization)
    user.pop("password_hash", None)
    return user

# ==================== TEST ROUTE ====================
@api_router.get("/test")
async def test():
    return {"message": "Backend is working ✅"}

# ==================== REGISTER ROUTER ====================
fastapi_app.include_router(api_router)

# ==================== CORS ====================
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== SOCKET WRAP ====================
app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app) 
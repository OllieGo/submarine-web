from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import hashlib
from jose import jwt
from datetime import datetime, timedelta

from data_handler.storage import DataStorage
from sqlalchemy import text

router = APIRouter(prefix="/api/auth", tags=["auth"])

SECRET_KEY = "submarine_quant_secret_key_2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

security = HTTPBearer()
storage = DataStorage()


def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


class UserRegister(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    phone: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


@router.post("/register")
async def register(user: UserRegister):
    import pandas as pd
    check_query = "SELECT id FROM user WHERE user_name = %s"
    df = pd.read_sql(check_query, storage.engine, params=(user.username,))
    if not df.empty:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pwd = hash_password(user.password)
    query = text("""
        INSERT INTO user (user_name, nick_name, password, email, phone)
        VALUES (:user_name, :nick_name, :password, :email, :phone)
    """)
    with storage.engine.begin() as conn:
        conn.execute(query, {
            'user_name': user.username,
            'nick_name': user.username,
            'password': hashed_pwd,
            'email': user.email,
            'phone': user.phone
        })
    return {"message": "User registered successfully"}


@router.post("/login")
async def login(user: UserLogin):
    import pandas as pd
    query = "SELECT id, user_name, nick_name, password, status FROM user WHERE user_name = %s"
    df = pd.read_sql(query, storage.engine, params=(user.username,))

    if df.empty:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    user_data = df.iloc[0].to_dict()

    if user_data['status'] != 1:
        raise HTTPException(status_code=401, detail="Account is disabled")

    if hash_password(user.password) != user_data['password']:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": user.username, "user_id": user_data['id']})
    return {"access_token": access_token, "token_type": "bearer", "username": user.username, "nick_name": user_data['nick_name']}


@router.get("/me")
async def get_current_user_info(username: str = Depends(get_current_user)):
    import pandas as pd
    query = "SELECT id, user_name, nick_name, email, phone, status, created_at FROM user WHERE user_name = %s"
    df = pd.read_sql(query, storage.engine, params=(username,))
    if df.empty:
        raise HTTPException(status_code=404, detail="User not found")
    return df.iloc[0].to_dict()
from datetime import datetime,timedelta
from jose import jwt 
from .crud import verify_password, get_user_by_username
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

def authenticate_user(db:Session,username:str,password:str):
    user = get_user_by_username(db,username)
    if not user:
        return None
    if not verify_password(password,user.hashed_password):
        return None
    return user

def create_access_token(data:dict,expires_delta:int=os.getenv("ACCESS_TOKEN_EXPIRE_MIN")):
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(minutes=expires_delta)
    return jwt.encode(to_encode,os.getenv("SECRET_KEY"),algorith=os.getenv("ALGORITHM"))
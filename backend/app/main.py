from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt 
from passlib.context import CryptContext
from .deps import get_db
from .crud import get_user_by_username, create_user
from .auth import authenticate_user, create_access_token

app = FastAPI(title="Core API")

class RegisterRequest(BaseModel):
    username:str
    email:str
    password:str

#C
@app.post("/register")
def register_user(req: RegisterRequest, db=Depends(get_db)):
    existing = get_user_by_username(db,req.username)
    if existing:
        raise HTTPException(409,"Username already exists")
    user = create_user(db,req.username, req.email, req.password)
    return {"id":user.id,"username":user.username}

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user = authenticate_user(db,form_data.username,form_data.password)
    if not user:
        raise HTTPException(401,"Invalid username or password")
    token = create_access_token({"sub":user.username})
    return {"access_token":token,"token_type":"bearer"}

@app.get("/secure-data")
def secure_data(token: str=Depends()):
    return {"secret":"You are authenticated"}
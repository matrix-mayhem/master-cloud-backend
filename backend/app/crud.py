from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .models import User

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

#R
def get_user_by_username(db: Session,username: str):
    return db.query(User).filter(User.username==username).first()

def get_user_by_email(db:Session,email:str):
    return db.query(User).filter(User.email==email).first()

#C
def create_user(db:Session,username:str,email:str,password:str):
    hashed = pwd_context.hash(password)
    new_user = User(username=username, email=email,password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def verify_password(plain, hashed):
    return pwd_context.verify(plain,hashed)


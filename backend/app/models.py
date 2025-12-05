from sqlalchemy import Column, Integer, DateTime, String
from datetime import datetime
from .db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True,nullable=False,index=True)
    username = Column(String,unique=True,nullable=False,index=True)
    email = Column(String,unique=True,nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime,default=datetime.utcnow)
from sqlalchemy import Column, Integer, String, DateTime, Float, BigInteger, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base
from app.database.database import Base

class Candle(Base):
    __tablename__ = "candles"

    symbol = Column(String, primary_key=True)
    timestamp = Column(DateTime, primary_key=True)

    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(BigInteger)

from sqlalchemy import Column, Integer, String, DateTime, Float, BigInteger, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base
from worker_database import Base

class Candle(Base):
    __tablename__ = "candles"

    symbol = Column(String, primary_key=True, index=True)
    timestamp = Column(DateTime, primary_key=True, index=True)

    open = Column(Float,nullable=False)
    high = Column(Float,nullable=False)
    low = Column(Float,nullable=False)
    close = Column(Float,nullable=False)
    volume = Column(Float,nullable=False)

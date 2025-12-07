from sqlalchemy import Column, String, Float, DateTime
from worker_database import Base

class Candle(Base):
    __tablename__ = "candles"

    symbol = Column(String, primary_key=True, index=True)
    timestamp = Column(DateTime, primary_key=True, index=True)

    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)

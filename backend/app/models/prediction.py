from sqlalchemy import Column, String, BigInteger, Float, DateTime
from app.database.database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    symbol = Column(String,primary_key=True)
    timestamp = Column(DateTime,primary_key=True)

    predicted_close = Column(Float)
    model_name = Column(String)
    confidence = Column(Float)
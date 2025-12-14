from sqlalchemy import Column, String, Float, DateTime
from app.database.finance_db import Base
from datetime import datetime


class AdasFrame(Base):
    __tablename__ = "adas_frames"

    timestamp = Column(DateTime, primary_key=True, index=True, default=datetime.utcnow)
    ego_speed = Column(Float, nullable=False)              # m/s or km/h
    lead_distance = Column(Float, nullable=False)          # meters
    detected_sign = Column(String, nullable=False)         # e.g. "SPEED_60", "STOP", "NONE"
    commanded_action = Column(String, nullable=False)      # "ACCELERATE", "MAINTAIN", "BRAKE"

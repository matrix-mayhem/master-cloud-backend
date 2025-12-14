from sqlalchemy import Column, String, Float, DateTime
from worker_database import Base
from datetime import datetime


class AdasFrame(Base):
    __tablename__ = "adas_frames"

    timestamp = Column(DateTime, primary_key=True, index=True, default=datetime.utcnow)
    ego_speed = Column(Float, nullable=False)
    lead_distance = Column(Float, nullable=False)
    detected_sign = Column(String, nullable=False)
    commanded_action = Column(String, nullable=False)

from sqlalchemy import Column, Integer, String, DateTime
from worker_database import Base
from datetime import datetime

class CanFrame(Base):
    __tablename__ = "can_frames"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    can_id = Column(Integer, nullable=False)
    data = Column(String, nullable=False)  # hex payload

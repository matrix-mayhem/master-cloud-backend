from sqlalchemy import Column, Integer, DateTime, LargeBinary
from worker_database import Base
from datetime import datetime


class CanFrame(Base):
    __tablename__ = "can_frames"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    can_id = Column(Integer, nullable=False)
    dlc = Column(Integer, nullable=False)
    payload = Column(LargeBinary, nullable=False)

from sqlalchemy import Column, Integer, LargeBinary, DateTime
from datetime import datetime
from worker_database import Base


class CanFrame(Base):
    __tablename__ = "can_frames"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    can_id = Column(Integer, nullable=False)
    dlc = Column(Integer, nullable=False)
    payload = Column(LargeBinary(8), nullable=False)

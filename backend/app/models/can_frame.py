from sqlalchemy import Column, Integer, DateTime, LargeBinary
from app.database.finance_db import Base
from datetime import datetime

class CanFrame(Base):
    __tablename__ = "can_frames"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    can_id = Column(Integer, nullable=False)
    dlc = Column(Integer, nullable=False)
    data = Column(LargeBinary, nullable=False)

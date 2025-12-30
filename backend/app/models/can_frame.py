from sqlalchemy import Column, Integer, DateTime, LargeBinary
from app.database.finance_db import Base
from datetime import datetime


class CanFrame(Base):
    __tablename__ = "can_frames"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    can_id = Column(Integer, nullable=False)      # e.g. 0x100 → 256
    dlc = Column(Integer, nullable=False)         # Data Length Code (0–8)
    payload = Column(LargeBinary, nullable=False) # 8 bytes

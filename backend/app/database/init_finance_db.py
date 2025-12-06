from .finance_db import Base, engine
from ..models.candle import Candle

Base.metadata.create_all(bind=engine)
print("Finance Tables are created")

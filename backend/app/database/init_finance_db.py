from backend.app.database.finance_db import Base, engine
from backend.app.models.candle import Candle

Base.metadata.create_all(bind=engine)
print("Finance Tables are created")

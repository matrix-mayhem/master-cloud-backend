from app.database.finance_db import Base, engine
from app.models.candle import Candle

Base.metadata.create_all(bind=engine)
print("✅ Finance tables created successfully")

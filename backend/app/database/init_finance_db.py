from app.database.finance_db import Base, engine
from app.models.candle import Candle
from app.models.adas_frame import AdasFrame

Base.metadata.create_all(bind=engine)
print("✅ Finance + ADAS tables created successfully")

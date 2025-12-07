from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@market-db:5432/market"
)

engine = create_engine(DATABASE_URL)

MarketSessionLocal = sessionmaker(bind=engine,autocommit=False,autoflush=False)

Base = declarative_base()
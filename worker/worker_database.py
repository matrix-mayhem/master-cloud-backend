from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

engine = create_engine(
    "DATABASE_URL","postgresql://user:password@market-db:5432/market"
)

MarketSessionLocal = sessionmaker(bind=engine,autocommit=False,autoflush=False)

Base = declarative_base()
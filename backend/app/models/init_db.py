from app.database.database import Base,engine
from candle import Candle
from prediction import Prediction

def init_db():
    print("Creating tables...")
    Base.metadata.create_engine(bind=engine)

if __name__ =="__main__":
    init_db()
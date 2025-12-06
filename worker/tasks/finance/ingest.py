import yfinance as yf
from datetime import datetime
from worker_database import MarketSessionLocal
from backend.app.models.candle import Candle

def ingest_ohlc(symbol="AAPL"):
    df = yf.download(symbol, period="5d",interval="1m")

    session = MarketSessionLocal()

    for idx, row in df.iterrows():
        candle = Candle(
            symbol=symbol,
            timestamp=idx.to_pydatetime(),
            open=row["Open"],
            high=row["High"],
            low=row["Low"],
            close=row["Close"],
            volume=row["Volume"]
        )
        session.merge(candle)
    
    session.commit()
    session.close()

    return {"status":"ok","symbol":symbol}
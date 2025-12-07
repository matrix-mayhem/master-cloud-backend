import yfinance as yf
from datetime import datetime
from worker_database import MarketSessionLocal
from backend.app.models.candle import Candle

def ingest_ohlc(symbol="AAPL"):
    print(f"Downloading {symbol} OHLC data")

    df = yf.download(symbol, period="5d",interval="1m")

    if df.empty:
        print("No data received")
        return{"status":"failed", "reason": "no data"}
    
    session = MarketSessionLocal()

    for idx, row in df.iterrows():
        candle = Candle(
            symbol=symbol,
            timestamp=idx.to_pydatetime(),
            open=float(row["Open"]),
            high=float(row["High"]),
            low=float(row["Low"]),
            close=float(row["Close"]),
            volume=float(row["Volume"])
        )
        session.merge(candle)
    
    session.commit()
    session.close()
    print(f"Stored {len(df)} candles for {symbol}")
    return {"status":"ok","symbol":symbol}
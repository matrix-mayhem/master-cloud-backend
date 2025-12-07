import yfinance as yf
from worker_database import MarketSessionLocal
from models.candle import Candle

def ingest_ohlc(symbol: str = "AAPL"):
    print(f"📊 Downloading {symbol} OHLC data...")
    df = yf.download(symbol, period="5d", interval="1m")

    if df.empty:
        print("❌ No data received")
        return {"status": "failed", "reason": "no data"}

    session = MarketSessionLocal()

    for idx, row in df.iterrows():
        candle = Candle(
            symbol=symbol,
            timestamp=idx.to_pydatetime(),
            open=float(row["Open"]) if not hasattr(row["Open"], "iloc") else float(row["Open"].iloc[0]),
            high=float(row["High"]) if not hasattr(row["High"], "iloc") else float(row["High"].iloc[0]),
            low=float(row["Low"]) if not hasattr(row["Low"], "iloc") else float(row["Low"].iloc[0]),
            close=float(row["Close"]) if not hasattr(row["Close"], "iloc") else float(row["Close"].iloc[0]),
            volume=float(row["Volume"]) if not hasattr(row["Volume"], "iloc") else float(row["Volume"].iloc[0]),
        )
        session.merge(candle)

    session.commit()
    session.close()
    print(f"✅ Stored {len(df)} candles for {symbol}")
    return {"status": "ok", "symbol": symbol, "rows": len(df)}

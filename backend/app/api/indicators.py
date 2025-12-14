from fastapi import APIRouter
from app.database.finance_db import SessionLocal
from app.models.candle import Candle
from app.utils.indicators import calculate_sma, calculate_ema, calculate_rsi
import pandas as pd

router = APIRouter()


@router.get("/indicators")
def get_indicators(symbol: str = "AAPL"):
    session = SessionLocal()

    candles = session.query(Candle) \
        .filter(Candle.symbol == symbol) \
        .order_by(Candle.timestamp.asc()) \
        .all()

    session.close()

    if len(candles) < 50:
        return {"error": "Not enough data"}

    df = pd.DataFrame([{
        "timestamp": c.timestamp,
        "close": c.close
    } for c in candles])

    close_series = df["close"]

    sma_20 = float(calculate_sma(close_series, 20))
    sma_50 = float(calculate_sma(close_series, 50))
    ema_20 = float(calculate_ema(close_series, 20))
    rsi_14 = float(calculate_rsi(close_series, 14))

    return {
        "symbol": symbol,
        "sma_20": round(sma_20, 2),
        "sma_50": round(sma_50, 2),
        "ema_20": round(ema_20, 2),
        "rsi_14": round(rsi_14, 2)
    }

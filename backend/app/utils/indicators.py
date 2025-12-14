import pandas as pd


def calculate_sma(series: pd.Series, window: int):
    return series.rolling(window=window).mean().iloc[-1]


def calculate_ema(series: pd.Series, window: int):
    return series.ewm(span=window, adjust=False).mean().iloc[-1]


def calculate_rsi(series: pd.Series, period: int = 14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi.iloc[-1]

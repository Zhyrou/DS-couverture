"""Indicator calculations for multiple timeframes."""
from __future__ import annotations

import numpy as np
import pandas as pd


def ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False).mean()


def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain, index=series.index).rolling(window=period).mean()
    avg_loss = pd.Series(loss, index=series.index).rolling(window=period).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift()).abs()
    low_close = (df["low"] - df["close"].shift()).abs()
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = ranges.max(axis=1)
    return true_range.rolling(window=period).mean()


def volume_delta(df: pd.DataFrame) -> pd.Series:
    close_change = df["close"].diff().fillna(0)
    direction = np.where(close_change >= 0, 1, -1)
    return df["volume"] * direction


def range_high_low(series: pd.Series, period: int = 20) -> pd.DataFrame:
    rolling_high = series.rolling(window=period).max()
    rolling_low = series.rolling(window=period).min()
    return pd.DataFrame({"range_high": rolling_high, "range_low": rolling_low})


def volatility_band(series: pd.Series, period: int = 20, multiplier: float = 2.0) -> pd.DataFrame:
    basis = series.rolling(window=period).mean()
    dev = series.rolling(window=period).std()
    upper = basis + multiplier * dev
    lower = basis - multiplier * dev
    return pd.DataFrame({"basis": basis, "upper": upper, "lower": lower})

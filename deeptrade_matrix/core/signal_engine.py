"""Signal generation across multiple timeframes."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Dict, List

import pandas as pd

from deeptrade_matrix.core import indicators

logger = logging.getLogger(__name__)


@dataclass
class SignalSnapshot:
    timeframe: str
    direction: str
    confidence: float
    reason: str


class SignalEngine:
    def __init__(self, risk_per_trade: float = 20.0) -> None:
        self.risk_per_trade = risk_per_trade

    def _trend_direction(self, df: pd.DataFrame, trend_period: int = 200) -> str:
        ema_series = indicators.ema(df["close"], trend_period)
        last_close = df["close"].iloc[-1]
        last_ema = ema_series.iloc[-1]
        if last_close > last_ema:
            return "BULLISH"
        if last_close < last_ema:
            return "BEARISH"
        return "NEUTRAL"

    def _momentum_bias(self, df: pd.DataFrame) -> str:
        ema_fast = indicators.ema(df["close"], 20)
        rsi_series = indicators.rsi(df["close"], 14)
        close = df["close"].iloc[-1]
        ema_val = ema_fast.iloc[-1]
        rsi_val = rsi_series.iloc[-1]
        if close > ema_val and rsi_val > 55:
            return "BULLISH"
        if close < ema_val and rsi_val < 45:
            return "BEARISH"
        return "NEUTRAL"

    def _volume_context(self, df: pd.DataFrame) -> str:
        vol_delta = indicators.volume_delta(df)
        avg_delta = vol_delta.tail(20).mean()
        return "BUY_SIDE" if avg_delta > 0 else "SELL_SIDE"

    def _volatility(self, df: pd.DataFrame) -> float:
        atr_series = indicators.atr(df, period=14)
        return float(atr_series.iloc[-1])

    def _local_range(self, df: pd.DataFrame) -> Dict[str, float]:
        range_df = indicators.range_high_low(df["close"], period=20)
        latest = range_df.iloc[-1]
        return {"high": float(latest["range_high"]), "low": float(latest["range_low"])}

    def _build_reason(self, trend: str, momentum: str, volume: str) -> str:
        return f"Trend {trend}, momentum {momentum}, volume {volume}"

    def evaluate(self, df_by_timeframe: Dict[str, pd.DataFrame]) -> List[SignalSnapshot]:
        signals: List[SignalSnapshot] = []
        for timeframe, df in df_by_timeframe.items():
            if len(df) < 50:
                logger.info("Skipping %s due to insufficient data", timeframe)
                continue
            trend = self._trend_direction(df)
            momentum = self._momentum_bias(df)
            volume = self._volume_context(df)
            volatility = self._volatility(df)
            local_range = self._local_range(df)

            direction = "NEUTRAL"
            confidence = 0.4

            if trend == momentum == "BULLISH":
                direction = "LONG"
                confidence = 0.75
            elif trend == momentum == "BEARISH":
                direction = "SHORT"
                confidence = 0.75
            elif trend != "NEUTRAL" and momentum != "NEUTRAL":
                direction = "NEUTRAL"
                confidence = 0.55

            reason = self._build_reason(trend, momentum, volume)
            reason += f" | ATR {volatility:.2f} | Range {local_range['low']:.0f}-{local_range['high']:.0f}"

            signals.append(
                SignalSnapshot(
                    timeframe=timeframe,
                    direction=direction,
                    confidence=confidence,
                    reason=reason,
                )
            )

        return signals

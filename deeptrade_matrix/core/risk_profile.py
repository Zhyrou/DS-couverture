"""Risk and position sizing utilities."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class PositionSizing:
    position_size: float
    stop_loss: float
    take_profit: float
    risk_reward: float
    risk_amount: float


def calculate_position(entry: float, stop: float, take_profit: float, balance: float, risk_per_trade: float, leverage: int = 1) -> PositionSizing:
    if stop == entry:
        raise ValueError("Stop loss cannot equal entry price")

    risk_per_unit = abs(entry - stop)
    size = (risk_per_trade * leverage) / risk_per_unit
    rr = abs(take_profit - entry) / risk_per_unit if risk_per_unit else 0.0

    return PositionSizing(
        position_size=round(size, 6),
        stop_loss=stop,
        take_profit=take_profit,
        risk_reward=round(rr, 2),
        risk_amount=risk_per_trade,
    )


def suggest_levels(last_close: float, atr_value: float) -> Dict[str, float]:
    stop = last_close - atr_value
    take_profit = last_close + 2 * atr_value
    return {"stop": round(stop, 2), "take_profit": round(take_profit, 2)}

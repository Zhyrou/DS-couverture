"""Market data feed using ccxt."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

import ccxt
import pandas as pd

logger = logging.getLogger(__name__)


@dataclass
class OHLCVEntry:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


class DataFeed:
    """Wrapper around ccxt for fetching OHLCV and ticker data."""

    def __init__(self, exchange_id: str = "kraken") -> None:
        self.exchange_id = exchange_id
        self.exchange = self._init_exchange()

    def _init_exchange(self) -> ccxt.Exchange:
        if not hasattr(ccxt, self.exchange_id):
            raise ValueError(f"Exchange {self.exchange_id} is not supported by ccxt")
        exchange_class = getattr(ccxt, self.exchange_id)
        return exchange_class({"enableRateLimit": True})

    def fetch_ohlcv(self, symbol: str, timeframe: str, limit: int = 200) -> pd.DataFrame:
        try:
            raw = self.exchange.fetch_ohlcv(symbol=symbol, timeframe=timeframe, limit=limit)
        except Exception as exc:  # pragma: no cover - network/path specific
            logger.error("Failed to fetch OHLCV: %s", exc)
            raise

        records: List[OHLCVEntry] = []
        for row in raw:
            records.append(
                OHLCVEntry(
                    timestamp=datetime.fromtimestamp(row[0] / 1000),
                    open=float(row[1]),
                    high=float(row[2]),
                    low=float(row[3]),
                    close=float(row[4]),
                    volume=float(row[5]),
                )
            )

        df = pd.DataFrame(records)
        df.set_index("timestamp", inplace=True)
        return df

    def fetch_ticker(self, symbol: str) -> Optional[dict]:
        try:
            return self.exchange.fetch_ticker(symbol)
        except Exception as exc:  # pragma: no cover - network/path specific
            logger.error("Failed to fetch ticker: %s", exc)
            return None

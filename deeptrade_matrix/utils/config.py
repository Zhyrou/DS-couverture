"""Configuration handling for DeepTrade Matrix Desk."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

DEFAULT_CONFIG = {
    "exchange": "kraken",
    "symbol": "BTC/USD",
    "timeframes": ["1m", "5m", "15m", "1h", "4h", "1d"],
    "risk_per_trade": 20.0,
    "account_balance": 2000.0,
    "margin_leverage": 10,
}


class ConfigManager:
    """Simple JSON backed configuration manager."""

    def __init__(self, data_dir: Path) -> None:
        self.data_dir = data_dir
        self.config_file = self.data_dir / "config.json"

    def ensure_default_config(self) -> None:
        if not self.config_file.exists():
            self.save(DEFAULT_CONFIG)

    def load(self) -> Dict[str, Any]:
        if not self.config_file.exists():
            self.ensure_default_config()
        with self.config_file.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def save(self, config: Dict[str, Any]) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        with self.config_file.open("w", encoding="utf-8") as handle:
            json.dump(config, handle, indent=2)

    def update(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        config = self.load()
        config.update(updates)
        self.save(config)
        return config

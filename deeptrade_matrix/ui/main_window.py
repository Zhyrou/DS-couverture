"""Main window layout."""
from __future__ import annotations

import logging
from typing import Dict

import pandas as pd
from PySide6 import QtCore, QtWidgets

from deeptrade_matrix.core.data_feed import DataFeed
from deeptrade_matrix.core.signal_engine import SignalEngine, SignalSnapshot
from deeptrade_matrix.core.risk_profile import calculate_position, suggest_levels
from deeptrade_matrix.ui.charts_panel import ChartsPanel
from deeptrade_matrix.ui.matrix_background import MatrixBackground
from deeptrade_matrix.ui.signals_panel import SignalsPanel
from deeptrade_matrix.ui.cycle_panel import CyclePanel
from deeptrade_matrix.utils.config import ConfigManager

logger = logging.getLogger(__name__)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, config_manager: ConfigManager) -> None:
        super().__init__()
        self.setWindowTitle("DeepTrade Matrix Desk")
        self.resize(1200, 800)

        self.config_manager = config_manager
        self.config = config_manager.load()
        self.data_feed = DataFeed(exchange_id=self.config["exchange"])
        self.signal_engine = SignalEngine(risk_per_trade=self.config["risk_per_trade"])

        central_widget = QtWidgets.QWidget()
        central_layout = QtWidgets.QVBoxLayout(central_widget)
        central_layout.setSpacing(8)

        self.matrix_bg = MatrixBackground()
        bg_layout = QtWidgets.QVBoxLayout()
        bg_layout.setContentsMargins(0, 0, 0, 0)
        bg_layout.addWidget(self.matrix_bg)

        self.charts_panel = ChartsPanel()
        self.signals_panel = SignalsPanel()
        self.cycle_panel = CyclePanel()

        content_layout = QtWidgets.QHBoxLayout()
        content_layout.addWidget(self.charts_panel, stretch=3)
        content_layout.addWidget(self.signals_panel, stretch=2)

        central_layout.addLayout(bg_layout)
        central_layout.addWidget(self.cycle_panel)
        central_layout.addLayout(content_layout)

        self.setCentralWidget(central_widget)

        self.refresh_timer = QtCore.QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_data)
        self.refresh_timer.start(60_000)  # 1 minute refresh

        self.refresh_data()

    def _load_timeframes(self) -> Dict[str, pd.DataFrame]:
        dataframes: Dict[str, pd.DataFrame] = {}
        for tf in self.config["timeframes"]:
            try:
                df = self.data_feed.fetch_ohlcv(self.config["symbol"], tf, limit=250)
                dataframes[tf] = df
            except Exception:
                logger.exception("Failed to load timeframe %s", tf)
        return dataframes

    def refresh_data(self) -> None:
        df_map = self._load_timeframes()
        if not df_map:
            return

        signals = self.signal_engine.evaluate(df_map)
        self.signals_panel.update_signals(signals)

        primary_tf = max(df_map.keys(), key=lambda tf: df_map[tf].index[-1])
        df_primary = df_map[primary_tf]
        last_close = df_primary["close"].iloc[-1]
        atr_val = self.signal_engine._volatility(df_primary)
        levels = suggest_levels(last_close, atr_val)
        position = calculate_position(
            entry=last_close,
            stop=levels["stop"],
            take_profit=levels["take_profit"],
            balance=self.config["account_balance"],
            risk_per_trade=self.config["risk_per_trade"],
            leverage=self.config.get("margin_leverage", 1),
        )

        self.signals_panel.update_risk(position)
        self.charts_panel.update_chart(df_primary.tail(120), signals)

        logger.info("Data refreshed with %d timeframes", len(df_map))

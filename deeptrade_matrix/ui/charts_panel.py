"""Lightweight chart display using PyQtGraph."""
from __future__ import annotations

from typing import Iterable

import pandas as pd
import pyqtgraph as pg
from PySide6 import QtWidgets

from deeptrade_matrix.core.signal_engine import SignalSnapshot


class ChartsPanel(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.plot_widget = pg.PlotWidget(background="k")
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.plot_widget.getPlotItem().getAxis("left").setPen(pg.mkPen("#00ff9c"))
        self.plot_widget.getPlotItem().getAxis("bottom").setPen(pg.mkPen("#00ff9c"))
        layout.addWidget(self.plot_widget)

        self.signals_label = QtWidgets.QLabel("Signals context")
        layout.addWidget(self.signals_label)

    def update_chart(self, df: pd.DataFrame, signals: Iterable[SignalSnapshot]) -> None:
        self.plot_widget.clear()
        if df.empty:
            return

        x = list(range(len(df)))
        pen = pg.mkPen(color="#00ff9c", width=2)
        self.plot_widget.plot(x, df["close"].tolist(), pen=pen)

        last_signal = next(iter(signals), None)
        if last_signal:
            self.signals_label.setText(
                f"Last signal {last_signal.direction} on {last_signal.timeframe} (conf {last_signal.confidence:.2f})"
            )

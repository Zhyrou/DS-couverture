"""Panel displaying signals and risk data."""
from __future__ import annotations

from typing import List

from PySide6 import QtWidgets

from deeptrade_matrix.core.risk_profile import PositionSizing
from deeptrade_matrix.core.signal_engine import SignalSnapshot


class SignalsPanel(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(6)

        self.signals_list = QtWidgets.QTreeWidget()
        self.signals_list.setHeaderLabels(["TF", "Dir", "Conf", "Reason"])
        self.signals_list.setColumnWidth(0, 60)
        layout.addWidget(self.signals_list)

        self.risk_label = QtWidgets.QLabel("Position sizing: -")
        layout.addWidget(self.risk_label)

    def update_signals(self, signals: List[SignalSnapshot]) -> None:
        self.signals_list.clear()
        for snapshot in signals:
            item = QtWidgets.QTreeWidgetItem([
                snapshot.timeframe,
                snapshot.direction,
                f"{snapshot.confidence:.2f}",
                snapshot.reason,
            ])
            self.signals_list.addTopLevelItem(item)
        self.signals_list.expandAll()

    def update_risk(self, position: PositionSizing) -> None:
        self.risk_label.setText(
            f"Size: {position.position_size} | SL: {position.stop_loss} | TP: {position.take_profit} | R/R: {position.risk_reward}"
        )

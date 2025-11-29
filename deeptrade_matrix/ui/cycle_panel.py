"""Display days since last Bitcoin halving."""
from __future__ import annotations

from datetime import datetime, timezone

from PySide6 import QtWidgets

HALVING_DATE = datetime(2024, 4, 20, tzinfo=timezone.utc)


class CyclePanel(QtWidgets.QLabel):
    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet("color: #00ff9c; padding: 4px;")
        self.setTextInteractionFlags(QtWidgets.Qt.TextSelectableByMouse)
        self.refresh()

    def refresh(self) -> None:
        now = datetime.now(timezone.utc)
        days = (now - HALVING_DATE).days
        self.setText(f"Days since 2024 halving: {days}")

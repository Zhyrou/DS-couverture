"""Simple Matrix-style animated background."""
from __future__ import annotations

import random

from PySide6 import QtCore, QtGui, QtWidgets


class MatrixBackground(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.columns = 120
        self.stream_positions = [random.randint(0, self.height()) for _ in range(self.columns)]
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(80)

    def _animate(self) -> None:
        self.stream_positions = [pos + random.randint(5, 25) for pos in self.stream_positions]
        self.update()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:  # noqa: N802
        super().resizeEvent(event)
        self.stream_positions = [random.randint(0, self.height()) for _ in range(self.columns)]

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:  # noqa: N802
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtGui.QColor(0, 0, 0))
        painter.setPen(QtGui.QPen(QtGui.QColor("#00ff9c")))

        width = self.width()
        column_width = max(4, width // self.columns)

        for idx, pos in enumerate(self.stream_positions):
            x = idx * column_width
            y_start = pos % (self.height() + 50)
            painter.drawText(x, y_start, "1010")

        painter.end()

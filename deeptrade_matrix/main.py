"""Application entry point for DeepTrade Matrix Desk."""
from __future__ import annotations

import sys
from pathlib import Path

from PySide6 import QtWidgets

from deeptrade_matrix.ui.main_window import MainWindow
from deeptrade_matrix.utils.config import ConfigManager
from deeptrade_matrix.utils.logger import configure_logging


APP_NAME = "DeepTrade Matrix Desk"


def _ensure_data_dir() -> Path:
    base_dir = Path.home() / ".deeptrade_matrix"
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir


def main() -> None:
    data_dir = _ensure_data_dir()
    log_file = data_dir / "deeptrade.log"
    configure_logging(log_file)

    config_manager = ConfigManager(data_dir)
    config_manager.ensure_default_config()

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName(APP_NAME)

    window = MainWindow(config_manager=config_manager)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

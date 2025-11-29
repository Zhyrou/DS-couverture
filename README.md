# DeepTrade Matrix Desk

Desktop scanner for BTC/USD with a light Matrix aesthetic. The app combines ccxt data, multi-timeframe indicators, and risk profiling to keep Alex on-plan with ~20 USD risk per trade.

## Features
- PySide6 UI with Matrix-like background, charts (PyQtGraph), signal list, and cycle info (days since 2024 halving).
- Multi-timeframe signal engine (trend vs EMA200, momentum via EMA20 + RSI, volume delta, ATR, 20-candle range).
- Risk module suggesting SL/TP from ATR and position sizing for fixed risk and leverage.
- JSON config stored in `~/.deeptrade_matrix/config.json` with exchange, symbol, and risk parameters.

## Running
```bash
pip install -r requirements.txt
python -m deeptrade_matrix.main
```

On Windows, double-click `run.bat` after installing the requirements.

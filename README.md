# DeepTrade Matrix Desk

Desktop scanner for BTC/USD with a light Matrix aesthetic. The app combines ccxt data, multi-timeframe indicators, and risk profiling to keep Alex on-plan with ~20 USD risk per trade.

## Features
- PySide6 UI with Matrix-like background, charts (PyQtGraph), signal list, and cycle info (days since 2024 halving).
- Multi-timeframe signal engine (trend vs EMA200, momentum via EMA20 + RSI, volume delta, ATR, 20-candle range).
- Risk module suggesting SL/TP from ATR and position sizing for fixed risk and leverage.
- JSON config stored in `~/.deeptrade_matrix/config.json` with exchange, symbol, and risk parameters.

## Download & install
1. Télécharger le projet :
   - via Git : `git clone <URL_REPO_GITHUB>` (ou utilisez votre fork), puis `cd DS-couverture`.
   - ou via l’interface GitHub : **Code > Download ZIP**, extraire l’archive puis ouvrir le dossier.
2. Installez les dépendances Python 3.11+ :
   ```bash
   pip install -r requirements.txt
   ```
3. (Optionnel) Vérifiez que le module se charge bien :
   ```bash
   python -m compileall deeptrade_matrix
   ```

## Running
```bash
python -m deeptrade_matrix.main
```

Sur Windows, double-cliquez `run.bat` après installation des dépendances.

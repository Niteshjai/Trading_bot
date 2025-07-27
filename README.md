# 📈 Logistic Regression-Based Trading Bot

This project implements an automated trading bot that uses a logistic regression model trained on historical price features to generate buy/sell signals for a stock (e.g., AAPL). The bot fetches real-time data, makes predictions, and places orders via the Kite Connect API.

---

## 🧰 Overview

### 1. `model.py`

* Fetches historical OHLCV data from TradingView.
* Trains a logistic regression model on daily return direction.
* Standardizes features with `StandardScaler`.
* Saves trained model (`linear_model.pkl`) and scaler (`scaler.pkl`) to disk.

### 2. `strategy.py`

* Loads the trained model and scaler.
* Fetches the last 5 days of daily price data.
* Predicts signal (1 = BUY, 0 = SELL) based on latest day's features.
* Places orders using Kite Connect API.
* Logs each trade with timestamp, action, price, and quantity.

### 3. `main.py`

* Uses the `schedule` module to run the strategy during market hours (Mon–Fri, 10:15–3:30).
* Executes `run_strategy()` if market is open.
* Saves trade logs into a JSON file (`paper_trades_log.json`).

---

## ⚙️ Setup

### Required Libraries

* `pandas`, `numpy`
* `scikit-learn`
* `joblib`
* `tvDatafeed`
* `kiteconnect`
* `schedule`, `logging`, `json`, `os`

### Environment Variables

Set the following environment variables securely:

* `TV_USERNAME` and `TV_PASSWORD` for TradingView
* `KITE_API_KEY` and `KITE_ACCESS_TOKEN` for Zerodha Kite

---

## 🚀 Run Instructions

### 1. Train the Model

```bash
python model.py
```

This will fetch historical data, train the logistic regression model, and save it.

### 2. Run the Bot

```bash
python main.py
```

The bot will check every 60 seconds and run the strategy only during market hours.

---

## 🔎 Strategy Logic

* Features: `[open, high, low, close, volume]`
* Target: `1 if next-day return > 0 else 0`
* If signal = 1 ➔ place a BUY order
* If signal = 0 ➔ place a SELL order
* Order size: 10 units (customizable)

---

## 📊 Trade Logging

All trades are stored in `paper_trades_log.json` with structure:

```json
{
  "timestamp": "YYYY-MM-DD HH:MM:SS",
  "symbol": "AAPL",
  "action": "BUY" or "SELL",
  "quantity": 10,
  "price": 123.45
}
```

---

## 👤 Author

**Nitesh Jaiswal**

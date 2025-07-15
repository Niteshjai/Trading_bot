import pandas as pd
import numpy as np
from tvDatafeed import TvDatafeed, Interval
from sklearn.preprocessing import StandardScaler
from Trading_bot.model import load_trained_model
from Trading_bot.log_data import trade_log
from kiteconnect import KiteConnect
from joblib import load
from datetime import datetime as dt
import logging
import os

# Load TradingView credentials from environment variables for security
username = os.getenv('TV_USERNAME', 'your_username')
password = os.getenv('TV_PASSWORD', 'your_password')

# Load Kite API credentials from environment variables
kite_api_key = os.getenv('KITE_API_KEY', 'your_api_key')
kite_access_token = os.getenv('KITE_ACCESS_TOKEN', 'your_access_token')

# Initialize KiteConnect
kite = KiteConnect(api_key=kite_api_key)
kite.set_access_token(kite_access_token)

# Initialize TradingView datafeed
tv = TvDatafeed(username, password)
ticker = 'AAPL'  # Ticker to trade

# Global trade log list to store executed trades
trade_log = []

def place_order(symbol, action, price, quantity):
    """
    Places a BUY or SELL market order using Kite API
    """
    transaction_type = kite.TRANSACTION_TYPE_BUY if action.upper() == "BUY" else kite.TRANSACTION_TYPE_SELL
    
    # Place market order
    order = kite.place_order(
        variety=kite.VARIETY_REGULAR,
        exchange=kite.EXCHANGE_NSE,
        tradingsymbol=symbol,
        transaction_type=transaction_type,
        quantity=quantity,
        product=kite.PRODUCT_CNC,
        order_type=kite.ORDER_TYPE_MARKET
    )
    
    # Log the trade
    log_trade(symbol, action, price, quantity)

def get_features():
    """
    Fetches latest market data and prepares features for model prediction
    """
    # Download last 5 daily candles from TradingView
    data = tv.get_hist(
        symbol=ticker,
        exchange='NASDAQ',
        interval=Interval.in_daily,
        n_bars=5
    )

    # Create binary target: 1 if return > 0, else 0
    data['return'] = (data['close'].pct_change() > 0).astype(int)
    data.dropna(inplace=True)  # Remove rows with NaNs

    # Select feature columns (must match training features)
    features = ['open', 'high', 'low', 'close', 'volume']
    X = data[features]

    # Load the pre-trained scaler from disk
    scaler = load("scaler.pkl")
    X_scaled = scaler.transform(X)  # Standardize features

    # Return the latest row of features for prediction and latest close price
    return X_scaled[-1].reshape(1, -1), data['close'].iloc[-1]

def run_strategy():
    """
    Runs the trading logic using the trained model and places order based on signal
    """
    # Load trained logistic regression model
    model = load_trained_model()

    # Get standardized features and current price
    features, price = get_features()

    # Predict signal (1 = Buy, 0 = Sell)
    signal = model.predict(features)[0]

    # Place the corresponding order
    action = 'BUY' if signal == 1 else 'SELL'
    place_order(ticker, action, price, 10)

def log_trade(symbol, action, price, quantity):
    """
    Records each executed trade into the trade log and logs info
    """
    trade_log.append({
        "timestamp": dt.now().strftime("%Y-%m-%d %H:%M:%S"),
        "symbol": symbol,
        "action": action,
        "quantity": quantity,
        "price": price
    })

    logging.info(f"{action} order placed for {symbol} at {price}")

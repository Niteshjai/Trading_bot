import pandas as pd
import numpy as np
from tvDatafeed import TvDatafeed, Interval
from sklearn.preprocessing import StandardScaler
from model import load_trained_model
from log_data import trade_log
from kiteconnect import KiteConnect, KiteTicker
import datetime
import logging

username = 'Niteshjai'
password = 'Niteshjaiswal1234'


kite = KiteConnect(api_key="your_api_key")
kite.set_access_token("your_access_token")

tv = TvDatafeed(username, password)
ticker='AAPL'
# Global trade log
trade_log = []

def place_order(symbol, action, price,quantity):
    transaction_type = kite.TRANSACTION_TYPE_BUY if action == "BUY" else kite.TRANSACTION_TYPE_SELL
    order = kite.place_order(
        variety=kite.VARIETY_REGULAR,
        exchange=kite.EXCHANGE_NSE,
        tradingsymbol=symbol,
        transaction_type=transaction_type,
        quantity=quantity,
        product=kite.PRODUCT_CNC,
        order_type=kite.ORDER_TYPE_MARKET
    )
    log_trade(symbol, action, price,quantity)
    

def get_features():
    data = tv.get_hist(
            symbol=ticker,
            exchange='NASDAQ',
            interval=Interval.in_daily,
            n_bars=5
        )
    data['return']=(data['close'].pct_change>0).astype(int)
    data.dropna(inplace=True)

    X=data.drop['return']
    scaler=StandardScaler()
    X=scaler.fit_transform(X)
    return X.iloc[-1],data['close'].iloc[-1]
    
def run_strategy():
    model=load_trained_model()
    features,price=get_features()
    signal=model.predict(features);

    if signal==1:
        place_order(ticker,'Buy',price,10)
    else:
        place_order(ticker,'SELL',price,10)

def log_trade(symbol, action, price,quantity):
    # Log the trade
    trade_log.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "symbol": symbol,
        "action": action,
        "quantity": quantity,
        "price": price
    })

    logging.info(f"{action} order placed for {symbol} at {price}")    
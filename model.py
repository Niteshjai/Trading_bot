import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from tvDatafeed import TvDatafeed, Interval
import joblib

username = 'Niteshjai'
password = 'Niteshjaiswal1234'

tv = TvDatafeed(username, password)

class model_training():
    def _init_(self,ticker):
        self.ticker=ticker

    def model_data(self):
        data = tv.get_hist(
            symbol=self.ticker,
            exchange='NASDAQ',
            interval=Interval.in_daily,
            from_date='2022-01-01',
            to_date='2025-06-01'
        )
        data['return']=(data['close'].pct_change>0).astype(int)
        data.dropna(inplace=True)
        X=data.drop['return']
        y=data['return']

        scaler=StandardScaler()
        X=scaler.fit_transform(X)
        return X,y

    def model(self):
        X,y=self.model_data()
        model=LogisticRegression()
        model.fit(X,y)

        joblib.dump(model, 'linear_model.pkl')
    
dt=model_training('AAPL')
dt.model()

def load_trained_model():
    return joblib.load('linear_model.pkl')


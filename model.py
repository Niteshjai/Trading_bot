import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from tvDatafeed import TvDatafeed, Interval
import joblib
import os

# Load TradingView credentials from environment variables for security
username = os.getenv('TV_USERNAME', 'your_username')
password = os.getenv('TV_PASSWORD', 'your_password')

# Initialize TradingView datafeed
tv = TvDatafeed(username, password)

class ModelTraining:
    """
    Class to fetch historical data, preprocess it, and train a logistic regression model.
    """

    def __init__(self, ticker):
        """
        Initialize with the ticker symbol.
        """
        self.ticker = ticker

    def model_data(self):
        """
        Fetches historical price data from TradingView and prepares features and labels.
        Returns:
            X_scaled (np.array): Scaled feature matrix
            y (pd.Series): Binary target (1 if next day return > 0, else 0)
        """
        # Download historical OHLCV data from TradingView
        data = tv.get_hist(
            symbol=self.ticker,
            exchange='NASDAQ',
            interval=Interval.in_daily,
            from_date='2022-01-01',
            to_date='2025-06-01'
        )

        # Create binary classification target based on positive daily returns
        data['return'] = (data['close'].pct_change() > 0).astype(int)
        data.dropna(inplace=True)  # Remove rows with NaN (first row after pct_change)

        # Select numerical columns as features
        features = ['open', 'high', 'low', 'close', 'volume']
        X = data[features]
        y = data['return']

        # Standardize features using StandardScaler
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Save the scaler for use during inference
        joblib.dump(scaler, 'scaler.pkl')

        return X_scaled, y

    def model(self):
        """
        Trains a logistic regression model on historical data and saves it to disk.
        """
        X, y = self.model_data()

        # Initialize and train the model
        model = LogisticRegression()
        model.fit(X, y)

        # Save the trained model for later use in trading
        joblib.dump(model, 'linear_model.pkl')
        print("Model trained and saved.")

# Train model on AAPL data
dt = ModelTraining('AAPL')
dt.model()

def load_trained_model():
    """
    Loads the saved logistic regression model from disk.
    Returns:
        Trained logistic regression model
    """
    return joblib.load('linear_model.pkl')

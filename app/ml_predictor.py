import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta
import yfinance as yf
from typing import Dict, List
from app.models import Prediction

class MLPredictor:
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.is_trained = {}
    
    def prepare_features(self, df: pd.DataFrame) -> np.ndarray:
        """Prepare features from stock data"""
        # Calculate technical indicators
        df['SMA_10'] = df['Close'].rolling(window=10).mean()
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['RSI'] = self.calculate_rsi(df['Close'])
        df['Volume_MA'] = df['Volume'].rolling(window=10).mean()
        
        # Price changes
        df['Price_Change'] = df['Close'].pct_change()
        df['High_Low_Pct'] = (df['High'] - df['Low']) / df['Close']
        
        # Select features
        features = ['Open', 'High', 'Low', 'Volume', 'SMA_10', 'SMA_20', 
                   'RSI', 'Volume_MA', 'Price_Change', 'High_Low_Pct']
        
        return df[features].dropna()
    
    def calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def train_model(self, symbol: str) -> bool:
        """Train ML model for a specific stock"""
        try:
            # Fetch historical data
            ticker = yf.Ticker(symbol)
            df = ticker.history(period="1y", interval="1d")
            
            if len(df) < 50:  # Need minimum data
                return False
            
            # Prepare features and target
            features_df = self.prepare_features(df)
            if len(features_df) < 20:
                return False
            
            X = features_df.values
            y = df['Close'].shift(-1).dropna().values[:len(X)]  # Next day price
            
            # Handle size mismatch
            min_len = min(len(X), len(y))
            X = X[:min_len]
            y = y[:min_len]
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Train model
            model = RandomForestRegressor(
                n_estimators=100,
                random_state=42,
                max_depth=10,
                min_samples_split=5
            )
            model.fit(X_train_scaled, y_train)
            
            # Store model and scaler
            self.models[symbol] = model
            self.scalers[symbol] = scaler
            self.is_trained[symbol] = True
            
            # Calculate accuracy
            score = model.score(X_test_scaled, y_test)
            print(f"📊 Model trained for {symbol} with R² score: {score:.3f}")
            
            return True
            
        except Exception as e:
            print(f"Error training model for {symbol}: {e}")
            return False
    
    def predict_price(self, symbol: str, horizon: str = "1d") -> Prediction:
        """Make price prediction"""
        try:
            if symbol not in self.models or not self.is_trained[symbol]:
                if not self.train_model(symbol):
                    return None
            
            # Get recent data
            ticker = yf.Ticker(symbol)
            df = ticker.history(period="3mo", interval="1d")
            
            features_df = self.prepare_features(df)
            if len(features_df) == 0:
                return None
            
            # Get latest features
            latest_features = features_df.iloc[-1:].values
            
            # Scale and predict
            model = self.models[symbol]
            scaler = self.scalers[symbol]
            
            scaled_features = scaler.transform(latest_features)
            predicted_price = model.predict(scaled_features)[0]
            
            # Calculate confidence (simplified)
            recent_prices = df['Close'].tail(10).values
            volatility = np.std(recent_prices)
            confidence = max(0.5, 1.0 - (volatility / np.mean(recent_prices)))
            
            return Prediction(
                symbol=symbol,
                predicted_price=float(predicted_price),
                confidence=float(confidence),
                prediction_horizon=horizon
            )
            
        except Exception as e:
            print(f"Error predicting price for {symbol}: {e}")
            return None
    
    async def generate_predictions(self) -> List[Prediction]:
        """Generate predictions for all tracked symbols"""
        predictions = []
        
        for symbol in ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']:
            prediction = self.predict_price(symbol)
            if prediction:
                predictions.append(prediction)
        
        return predictions

# Global ML predictor instance
ml_predictor = MLPredictor()
__version__ = "1.0.0"
__author__ = "Stock Trading System Team"
__description__ = "Real-time stock market analysis and prediction system"

# Import main components for easy access
from .main import app
from .models import StockPrice, PriceAlert, Prediction, Transaction
from .websocket_manager import manager as websocket_manager
from .data_fetcher import data_fetcher
from .ml_predictor import ml_predictor
from .alert_system import alert_system
from .telegram_bot import telegram_bot

# Package metadata
__all__ = [
    "app",
    "StockPrice",
    "PriceAlert", 
    "Prediction",
    "Transaction",
    "websocket_manager",
    "data_fetcher",
    "ml_predictor",
    "alert_system",
    "telegram_bot"
]

# System status
SYSTEM_STATUS = {
    "name": "Stock Trading System",
    "version": __version__,
    "status": "running",
    "components": [
        "FastAPI Web Server",
        "WebSocket Manager", 
        "Real-time Data Fetcher",
        "ML Price Predictor",
        "Alert System",
        "Telegram Bot"
    ]
}

def get_system_info():
    """Get system information and status"""
    return SYSTEM_STATUS

def get_version():
    """Get current version"""
    return __version__
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/stockdb")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # APIs
    ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    
    # App
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    
    # Stock symbols to track
    STOCK_SYMBOLS = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
    
    # Update intervals
    DATA_UPDATE_INTERVAL = 60  # seconds
    PREDICTION_INTERVAL = 300  # seconds

settings = Settings()

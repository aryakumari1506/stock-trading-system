from .settings import Settings, settings

__version__ = "1.0.0"
__all__ = ["Settings", "settings"]

# Configuration constants
DEFAULT_CONFIG = {
    "APP_NAME": "Stock Trading System",
    "APP_VERSION": "1.0.0",
    "DEFAULT_SYMBOLS": ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"],
    "UPDATE_INTERVALS": {
        "data_fetch": 60,  # seconds
        "ml_prediction": 300,  # seconds
        "health_check": 30  # seconds
    },
    "LIMITS": {
        "max_alerts_per_user": 50,
        "max_websocket_connections": 1000,
        "api_rate_limit": 100  # requests per minute
    },
    "FEATURES": {
        "real_time_data": True,
        "ml_predictions": True,
        "price_alerts": True,
        "telegram_notifications": True,
        "web_dashboard": True
    }
}

def get_default_config():
    """Get default configuration dictionary"""
    return DEFAULT_CONFIG.copy()

def validate_config(config_dict):
    """Validate configuration dictionary"""
    required_fields = ["MONGODB_URL", "REDIS_URL"]
    
    for field in required_fields:
        if not config_dict.get(field):
            raise ValueError(f"Required configuration field '{field}' is missing")
    
    return True

# Export configuration
config = get_default_config()
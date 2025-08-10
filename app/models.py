from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel

class StockPrice(BaseModel):
    symbol: str
    price: float
    volume: int
    timestamp: datetime
    change_percent: Optional[float] = None
    
class PriceAlert(BaseModel):
    symbol: str
    target_price: float
    condition: str  # "above" or "below"
    user_id: str
    is_active: bool = True
    created_at: datetime = datetime.now()

class Prediction(BaseModel):
    symbol: str
    predicted_price: float
    confidence: float
    prediction_horizon: str  # "1h", "1d", "1w"
    timestamp: datetime = datetime.now()

class Transaction(BaseModel):
    symbol: str
    action: str  # "buy" or "sell"
    quantity: int
    price: float
    user_id: str
    timestamp: datetime = datetime.now()
import asyncio
import yfinance as yf
import requests
from datetime import datetime
from typing import Dict, List
from config.settings import settings
from app.models import StockPrice
from app.websocket_manager import manager

class DataFetcher:
    def __init__(self):
        self.running = False
    
    def fetch_yahoo_data(self, symbol: str) -> Dict:
        """Fetch real-time stock data from Yahoo Finance"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="1d", interval="1m")
            
            if not hist.empty:
                latest = hist.iloc[-1]
                current_price = float(latest['Close'])
                volume = int(latest['Volume'])
                
                # Calculate change percentage
                if len(hist) > 1:
                    prev_price = float(hist.iloc[-2]['Close'])
                    change_percent = ((current_price - prev_price) / prev_price) * 100
                else:
                    change_percent = 0.0
                
                return {
                    "symbol": symbol,
                    "price": current_price,
                    "volume": volume,
                    "change_percent": change_percent,
                    "timestamp": datetime.now()
                }
        except Exception as e:
            print(f"Error fetching Yahoo data for {symbol}: {e}")
            return None
    
    def fetch_alpha_vantage_data(self, symbol: str) -> Dict:
        """Fetch data from Alpha Vantage API"""
        if not settings.ALPHA_VANTAGE_API_KEY:
            return None
            
        try:
            url = f"https://www.alphavantage.co/query"
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": symbol,
                "apikey": settings.ALPHA_VANTAGE_API_KEY
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if "Global Quote" in data:
                quote = data["Global Quote"]
                return {
                    "symbol": symbol,
                    "price": float(quote["05. price"]),
                    "volume": int(quote["06. volume"]),
                    "change_percent": float(quote["10. change percent"].rstrip('%')),
                    "timestamp": datetime.now()
                }
        except Exception as e:
            print(f"Error fetching Alpha Vantage data for {symbol}: {e}")
            return None
    
    async def fetch_stock_data(self, symbol: str) -> StockPrice:
        """Fetch stock data with fallback sources"""
        # Try Yahoo Finance first (free and reliable)
        data = self.fetch_yahoo_data(symbol)
        
        # Fallback to Alpha Vantage if Yahoo fails
        if not data and settings.ALPHA_VANTAGE_API_KEY:
            data = self.fetch_alpha_vantage_data(symbol)
        
        if data:
            return StockPrice(**data)
        return None
    
    async def start_data_streaming(self):
        """Start continuous data fetching and broadcasting"""
        self.running = True
        print("🚀 Starting real-time data streaming...")
        
        while self.running:
            try:
                # Fetch data for all symbols
                tasks = [self.fetch_stock_data(symbol) for symbol in settings.STOCK_SYMBOLS]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Process results and broadcast
                for result in results:
                    if isinstance(result, StockPrice):
                        # Broadcast to WebSocket clients
                        await manager.broadcast({
                            "type": "stock_update",
                            "data": result.dict()
                        })
                        
                        # Publish to Redis for other services
                        await manager.publish_to_redis(
                            "stock_updates", 
                            result.dict()
                        )
                
                # Wait before next update
                await asyncio.sleep(settings.DATA_UPDATE_INTERVAL)
                
            except Exception as e:
                print(f"Error in data streaming: {e}")
                await asyncio.sleep(5)  # Wait before retry
    
    def stop_data_streaming(self):
        """Stop data streaming"""
        self.running = False
        print("⏹️ Stopping data streaming...")

# Global data fetcher instance
data_fetcher = DataFetcher()
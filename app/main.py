import asyncio
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import redis.asyncio as redis
from pymongo import MongoClient
from datetime import datetime
from typing import List

from config.settings import settings
from app.models import StockPrice, PriceAlert, Prediction, Transaction
from app.websocket_manager import manager
from app.data_fetcher import data_fetcher
from app.ml_predictor import ml_predictor
from app.alert_system import alert_system
from app.telegram_bot import telegram_bot

# Initialize FastAPI app
app = FastAPI(
    title="Real-Time Stock Trading System",
    description="A distributed system for live stock data streaming and AI predictions",
    version="1.0.0"
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Global variables
mongodb_client = None
redis_client = None

# Startup event
@app.on_event("startup")
async def startup_event():
    global mongodb_client, redis_client
    
    print("🚀 Starting Stock Trading System...")
    
    # Initialize MongoDB
    try:
        mongodb_client = MongoClient(settings.MONGODB_URL)
        mongodb_client.admin.command('ping')
        print("✅ Connected to MongoDB")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
    
    # Initialize Redis
    try:
        redis_client = redis.from_url(settings.REDIS_URL)
        await redis_client.ping()
        print("✅ Connected to Redis")
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
    
    # Start background tasks
    asyncio.create_task(data_fetcher.start_data_streaming())
    asyncio.create_task(prediction_scheduler())
    print("✅ Background tasks started")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    print("⏹️ Shutting down Stock Trading System...")
    data_fetcher.stop_data_streaming()
    if redis_client:
        await redis_client.close()
    if mongodb_client:
        mongodb_client.close()

# Background task for ML predictions
async def prediction_scheduler():
    while True:
        try:
            # Generate predictions every 5 minutes
            predictions = await ml_predictor.generate_predictions()
            
            if predictions:
                # Broadcast predictions
                await manager.broadcast({
                    "type": "predictions",
                    "data": [pred.dict() for pred in predictions]
                })
                
                # Send to Telegram (once per hour)
                current_hour = datetime.now().hour
                if current_hour in [9, 12, 16]:  # Market hours
                    await telegram_bot.send_market_summary(predictions)
            
            await asyncio.sleep(settings.PREDICTION_INTERVAL)
            
        except Exception as e:
            print(f"Error in prediction scheduler: {e}")
            await asyncio.sleep(60)

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            # Echo back or process commands
            await manager.send_personal_message(
                {"type": "echo", "message": f"Received: {data}"}, 
                websocket
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# REST API Endpoints

@app.get("/")
async def root():
    return {"message": "Real-Time Stock Trading System API", "status": "running"}

@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard():
    """Serve the real-time dashboard"""
    with open("static/dashboard.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/api/stocks", response_model=List[dict])
async def get_current_stocks():
    """Get current stock prices"""
    try:
        # This would typically fetch from database
        # For demo, return sample data
        return [
            {
                "symbol": "AAPL",
                "price": 150.25,
                "change_percent": 1.2,
                "timestamp": datetime.now().isoformat()
            },
            {
                "symbol": "GOOGL", 
                "price": 2750.30,
                "change_percent": -0.8,
                "timestamp": datetime.now().isoformat()
            }
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/alerts")
async def create_alert(alert: PriceAlert):
    """Create a new price alert"""
    try:
        success = alert_system.add_alert(alert)
        if success:
            return {"message": "Alert created successfully", "alert": alert.dict()}
        else:
            raise HTTPException(status_code=400, detail="Failed to create alert")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/alerts/{user_id}")
async def get_user_alerts(user_id: str):
    """Get all active alerts for a user"""
    try:
        alerts = alert_system.get_active_alerts(user_id)
        return {"alerts": [alert.dict() for alert in alerts]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/alerts/{symbol}/{user_id}")
async def delete_alert(symbol: str, user_id: str):
    """Delete alerts for specific symbol and user"""
    try:
        success = alert_system.remove_alert(symbol, user_id)
        if success:
            return {"message": f"Alerts removed for {symbol}"}
        else:
            return {"message": "No alerts found to remove"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/predictions")
async def get_predictions():
    """Get latest AI predictions"""
    try:
        predictions = await ml_predictor.generate_predictions()
        return {"predictions": [pred.dict() for pred in predictions if pred]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/transactions")
async def create_transaction(transaction: Transaction):
    """Process a new transaction"""
    try:
        # Here you would typically save to database and process
        # For demo, just return success
        return {
            "message": "Transaction processed successfully",
            "transaction": transaction.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "redis": "connected" if redis_client else "disconnected",
            "mongodb": "connected" if mongodb_client else "disconnected",
            "data_fetcher": "running" if data_fetcher.running else "stopped"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )

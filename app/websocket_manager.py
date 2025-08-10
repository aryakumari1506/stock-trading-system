import json
import asyncio
from typing import List, Dict
from fastapi import WebSocket
import redis.asyncio as redis
from config.settings import settings

class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.redis_client = None
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        
        # Initialize Redis client if not exists
        if not self.redis_client:
            self.redis_client = redis.from_url(settings.REDIS_URL)
    
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        try:
            await websocket.send_text(json.dumps(message))
        except:
            self.disconnect(websocket)
    
    async def broadcast(self, message: dict):
        if self.active_connections:
            disconnected = []
            for connection in self.active_connections:
                try:
                    await connection.send_text(json.dumps(message))
                except:
                    disconnected.append(connection)
            
            # Remove disconnected clients
            for conn in disconnected:
                self.disconnect(conn)
    
    async def publish_to_redis(self, channel: str, message: dict):
        if self.redis_client:
            await self.redis_client.publish(channel, json.dumps(message))
    
    async def subscribe_to_redis(self, channel: str):
        if self.redis_client:
            pubsub = self.redis_client.pubsub()
            await pubsub.subscribe(channel)
            return pubsub
        return None

# Global WebSocket manager instance
manager = WebSocketManager()
import asyncio
from telegram import Bot
from telegram.error import TelegramError
from config.settings import settings
from app.models import Prediction
from typing import List

class TelegramBot:
    def __init__(self):
        self.bot = None
        if settings.TELEGRAM_BOT_TOKEN:
            self.bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    
    async def send_message(self, chat_id: str, message: str):
        """Send message to Telegram chat"""
        if not self.bot:
            print("Telegram bot not configured")
            return False
        
        try:
            await self.bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode='Markdown'
            )
            return True
        except TelegramError as e:
            print(f"Telegram error: {e}")
            return False
    
    async def send_market_summary(self, predictions: List[Prediction]):
        """Send daily market summary with predictions"""
        if not predictions or not settings.TELEGRAM_CHAT_ID:
            return
        
        message = "📊 **Daily Market Predictions** 📊\n\n"
        
        for pred in predictions:
            confidence_emoji = "🟢" if pred.confidence > 0.7 else "🟡" if pred.confidence > 0.5 else "🔴"
            
            message += f"{confidence_emoji} **{pred.symbol}**\n"
            message += f"   💰 Predicted: ${pred.predicted_price:.2f}\n"
            message += f"   🎯 Confidence: {pred.confidence*100:.1f}%\n"
            message += f"   ⏱️ Horizon: {pred.prediction_horizon}\n\n"
        
        message += f"🕒 Generated at: {predictions[0].timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        
        await self.send_message(settings.TELEGRAM_CHAT_ID, message)

# Global telegram bot instance
telegram_bot = TelegramBot()
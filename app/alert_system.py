import asyncio
from typing import List, Dict
from datetime import datetime
from app.models import PriceAlert, StockPrice
from app.telegram_bot import telegram_bot

class AlertSystem:
    def __init__(self):
        self.alerts: List[PriceAlert] = []
        self.running = False
    
    def add_alert(self, alert: PriceAlert) -> bool:
        """Add a new price alert"""
        try:
            self.alerts.append(alert)
            print(f"🔔 Alert added: {alert.symbol} {alert.condition} ${alert.target_price}")
            return True
        except Exception as e:
            print(f"Error adding alert: {e}")
            return False
    
    def remove_alert(self, symbol: str, user_id: str) -> bool:
        """Remove alerts for specific symbol and user"""
        try:
            initial_count = len(self.alerts)
            self.alerts = [
                alert for alert in self.alerts 
                if not (alert.symbol == symbol and alert.user_id == user_id)
            ]
            removed_count = initial_count - len(self.alerts)
            print(f"🗑️ Removed {removed_count} alerts for {symbol}")
            return removed_count > 0
        except Exception as e:
            print(f"Error removing alert: {e}")
            return False
    
    def check_alerts(self, stock_data: StockPrice) -> List[PriceAlert]:
        """Check if any alerts should be triggered"""
        triggered_alerts = []
        
        for alert in self.alerts[:]:  # Copy list to avoid modification issues
            if not alert.is_active or alert.symbol != stock_data.symbol:
                continue
            
            should_trigger = False
            
            if alert.condition == "above" and stock_data.price >= alert.target_price:
                should_trigger = True
            elif alert.condition == "below" and stock_data.price <= alert.target_price:
                should_trigger = True
            
            if should_trigger:
                triggered_alerts.append(alert)
                # Deactivate alert after triggering
                alert.is_active = False
        
        return triggered_alerts
    
    async def send_alert_notification(self, alert: PriceAlert, current_price: float):
        """Send alert notification via Telegram"""
        try:
            message = f"""
🚨 **PRICE ALERT TRIGGERED** 🚨

📈 Symbol: {alert.symbol}
💰 Target Price: ${alert.target_price:.2f}
📊 Current Price: ${current_price:.2f}
⚡ Condition: {alert.condition.upper()}
🕒 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Alert has been deactivated.
            """
            
            await telegram_bot.send_message(alert.user_id, message.strip())
            print(f"📱 Alert notification sent for {alert.symbol}")
            
        except Exception as e:
            print(f"Error sending alert notification: {e}")
    
    async def process_stock_update(self, stock_data: StockPrice):
        """Process incoming stock data and check for alerts"""
        triggered_alerts = self.check_alerts(stock_data)
        
        for alert in triggered_alerts:
            await self.send_alert_notification(alert, stock_data.price)
    
    def get_active_alerts(self, user_id: str = None) -> List[PriceAlert]:
        """Get all active alerts, optionally filtered by user"""
        if user_id:
            return [alert for alert in self.alerts if alert.is_active and alert.user_id == user_id]
        return [alert for alert in self.alerts if alert.is_active]

# Global alert system instance
alert_system = AlertSystem()
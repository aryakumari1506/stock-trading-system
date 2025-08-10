# stock-trading-system

# 📊 Real-Time Stock Trading System

A distributed real-time system that streams live stock market data, processes transactions instantly, and generates AI-powered price predictions. Built with a completely free tech stack.

## 🚀 Features

- **📈 Live Stock Data** - Real-time price streaming from Yahoo Finance
- **🤖 AI Predictions** - Machine learning price forecasting with confidence scores
- **🔔 Price Alerts** - Custom threshold notifications via Telegram
- **📊 Interactive Dashboard** - Real-time web interface with live updates
- **🌐 RESTful API** - Complete CRUD operations with auto-documentation
- **⚡ WebSocket Streaming** - Instant data broadcasting to all connected clients

## 🛠 Tech Stack (100% Free)

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | FastAPI + Python | Web framework and API |
| **Real-time** | WebSockets + Redis | Live data streaming |
| **Database** | MongoDB Atlas | Data storage (free tier) |
| **AI/ML** | Scikit-learn | Price predictions |
| **Data Source** | Yahoo Finance API | Stock market data |
| **Notifications** | Telegram Bot API | Price alerts |
| **Deployment** | Render/Railway | Hosting (free tier) |

## 🏗 Quick Start

### 1. Clone & Setup
```bash
git clone <your-repo>
cd stock-trading-system
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Setup
Create `.env` file:
```env
# Required
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/stockdb
REDIS_URL=redis://localhost:6379

# Optional
ALPHA_VANTAGE_API_KEY=your_api_key
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

### 3. Start Services
```bash
# Start Redis (using Docker)
docker-compose up -d redis

# Or install Redis locally and start it
```

### 4. Run Application
```bash
python app/main.py
```

### 5. Access Dashboard
- **Dashboard**: http://localhost:8000/dashboard
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📁 Project Structure

```
stock-trading-system/
├── app/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Data models
│   ├── websocket_manager.py # WebSocket handling
│   ├── data_fetcher.py      # Stock data collection
│   ├── ml_predictor.py      # AI prediction engine
│   ├── alert_system.py      # Price alerts
│   └── telegram_bot.py      # Telegram integration
├── config/
│   └── settings.py          # Configuration
├── static/
│   └── dashboard.html       # Web dashboard
├── docker/
│   └── docker-compose.yml   # Redis setup
├── requirements.txt         # Dependencies
└── .env                     # Environment variables
```

## 🔧 Configuration

### Stock Symbols
Edit `config/settings.py` to change tracked stocks:
```python
STOCK_SYMBOLS = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
```

### Update Intervals
```python
DATA_UPDATE_INTERVAL = 60    # Stock data refresh (seconds)
PREDICTION_INTERVAL = 300    # AI predictions (seconds)
```

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API status |
| GET | `/dashboard` | Web dashboard |
| GET | `/api/stocks` | Current stock prices |
| GET | `/api/predictions` | AI predictions |
| POST | `/api/alerts` | Create price alert |
| GET | `/api/alerts/{user_id}` | Get user alerts |
| DELETE | `/api/alerts/{symbol}/{user_id}` | Remove alert |
| GET | `/health` | System health check |

## 🚨 Setting Up Alerts

### Telegram Bot Setup
1. Message [@BotFather](https://t.me/botfather)
2. Create bot with `/newbot`
3. Get bot token
4. Get your chat ID by messaging [@userinfobot](https://t.me/userinfobot)
5. Add tokens to `.env` file

### Creating Alerts
```bash
curl -X POST http://localhost:8000/api/alerts \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "target_price": 150.0,
    "condition": "above",
    "user_id": "your_user_id"
  }'
```

## 🤖 AI Predictions

The system uses Random Forest regression with technical indicators:
- **Simple Moving Averages** (10-day, 20-day)
- **RSI** (Relative Strength Index)
- **Volume Analysis**
- **Price Change Patterns**

Confidence scores indicate prediction reliability (50-100%).

## 🐳 Docker Deployment

### Using Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Individual Services
```bash
# Redis only
docker run -d -p 6379:6379 redis:alpine

# MongoDB (if not using Atlas)
docker run -d -p 27017:27017 mongo:latest
```

## 🌐 Cloud Deployment

### Render (Recommended)
1. Connect GitHub repository
2. Create new Web Service
3. Set environment variables
4. Deploy automatically

### Railway
```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

### Vercel
```bash
npm install -g vercel
vercel --prod
```

## 📱 Using the Dashboard

1. **Connect** - Dashboard auto-connects via WebSocket
2. **View Stocks** - Real-time prices update every minute
3. **Monitor Predictions** - AI forecasts with confidence scores
4. **Set Alerts** - Create price threshold notifications
5. **Track Activity** - Monitor system events in real-time

## 🔍 Troubleshooting

### Common Issues

**WebSocket Connection Failed**
- Check if server is running on correct port
- Verify firewall settings
- Try different browser

**No Stock Data**
- Yahoo Finance may be rate limiting
- Add Alpha Vantage API key to `.env`
- Check internet connection

**Redis Connection Error**
```bash
# Check if Redis is running
docker ps
# Or
redis-cli ping
```

**MongoDB Connection Error**
- Verify connection string in `.env`
- Check MongoDB Atlas network access
- Ensure database user has correct permissions

### Performance Tips
- Use MongoDB Atlas for better performance
- Enable Redis persistence for alert storage
- Add more symbols gradually to avoid rate limits
- Monitor API usage to stay within free tiers

## 📈 Future Enhancements

- [ ] Portfolio tracking and management
- [ ] Advanced technical analysis indicators
- [ ] Social trading features
- [ ] Mobile app (React Native/Flutter)
- [ ] Advanced charting with candlesticks
- [ ] Multi-timeframe analysis
- [ ] Risk management tools

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🎯 Support

- **Issues**: Create GitHub issue for bugs
- **Discussions**: Use GitHub Discussions for questions
- **Email**: your-email@example.com

---

**⭐ Star this repository if it helped you!**

Built with ❤️ using 100% free and open-source technologies.

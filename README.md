🚀 Overview

PricePulse is a lightweight price-tracking platform that monitors Amazon product prices and alerts users when prices drop below a target value.

This project evolved from a simple scraping script into a modular MVP platform featuring:

✅ Telegram Bot interface

✅ REST API backend

✅ Persistent tracking database

✅ Multi-product tracking per user

✅ Clean service-oriented architecture

🎯 Features
Core Tracking

Track Amazon product prices

Set custom target price

Multi-product tracking

Persistent storage

Telegram Bot

/track <url> <price> — start tracking

/list — view active trackers

/stop <id> — stop tracking

/help — show commands

REST API

Fetch current price

Create trackers programmatically

Trigger price checks

🏗 Architecture
User (Telegram / Web)
        │
        ▼
     Flask API
        │
        ▼
   Service Layer
        │
 ┌──────┴────────┐
 ▼               ▼
Scraper       SQLite DB
(Amazon)   (products + trackers)
📁 Project Structure
amazon-price-tracker/
│
├── tracker/
│   ├── scraper.py      # Amazon scraping logic
│   ├── service.py      # Business logic
│   ├── storage.py      # SQLite persistence
│   └── __init__.py
│
├── bot/
│   └── telegram_bot.py # Telegram interface
│
├── web/
│   └── app.py          # Flask API
│
├── requirements.txt
└── README.md
⚙️ Local Setup
1️⃣ Clone Repository
git clone https://github.com/singhajeet79/amazon-price-tracker.git
cd amazon-price-tracker
2️⃣ Create Virtual Environment
python3 -m venv .venv
source .venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Initialize Database
python - <<EOF
from tracker.storage import init_db
init_db()
EOF
🤖 Telegram Bot Setup
Create Bot

Open Telegram → @BotFather

Run:

/newbot

Copy the bot token.

Configure Token

Edit:

bot/telegram_bot.py
BOT_TOKEN = "YOUR_TOKEN_HERE"
Run Bot
export PYTHONPATH=$(pwd)
python bot/telegram_bot.py
Bot Commands
/start
/help
/track <amazon_url> <target_price>
/list
/stop <tracker_id>

Example:

/track https://www.amazon.in/dp/B0FLJY793G 16000
🌐 Run REST API
export PYTHONPATH=$(pwd)
python web/app.py

Server:

http://127.0.0.1:5000
API Endpoints
Health Check
GET /
Get Current Price
POST /api/price
{
  "url": "https://www.amazon.in/dp/PRODUCT_ID"
}
Start Tracking
POST /api/track
{
  "url": "...",
  "target_price": 16000,
  "channel": "telegram",
  "contact": "chat_id"
}
🧠 How It Works

User submits product URL.

Scraper extracts title + price.

Product stored in SQLite.

Tracker linked to user.

Background checks compare price vs target.

Alert sent when price drops.

⚠️ Important Notes

Bot works only while the application is running.

Current version uses polling mode (not webhooks).

Amazon HTML structure may change over time.

🗺 Roadmap
Phase 2 (MVP)

 Modular architecture

 Telegram bot UX

 REST API

 Background scheduler

 Email notifications

Phase 3

 Docker deployment

 Web dashboard

 Price history graphs

 Multi-store support

Phase 4

 Webhook mode

 Cloud deployment

 Affiliate integrations

🧑‍💻 Author

Ajeet Singh

DevOps • Cloud • Platform Engineering

GitHub:
https://github.com/singhajeet79

📜 License

MIT License
---
### Be sure to **stargaze** the repository and check out [My GitHub Page](https://singhajeet79.github.io/) to contact me. Thank you!
#### Thank You.

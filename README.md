# 📉 PricePulse — Amazon Price Tracker

Minimal price-tracking platform that monitors Amazon products and sends alerts via a Telegram bot.

Built as a DevOps + backend engineering showcase: API, bot integration, persistence, and deployable architecture.

---

## ✨ Features

- Track Amazon product prices
- Telegram bot alerts
- REST API (Flask)
- Multi-product tracking
- SQLite persistence
- Docker & Kubernetes ready

---

## 🧱 Architecture
Telegram / API
│
▼
Flask API
│
Service Layer
│
Scraper ─── SQLite

---

## ⚡ Quick Start (1 minute)

```bash
git clone https://github.com/singhajeet79/amazon-price-tracker.git
cd amazon-price-tracker

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

Initialize DB:
python - <<EOF
from tracker.storage import init_db
init_db()
EOF
```
---

## 🤖 Run Telegram Bot

Create bot via @BotFather and set token in:
bot/telegram_bot.py

Run:
export PYTHONPATH=$(pwd)
python bot/telegram_bot.py

Commands:
/track <url> <price>
/list
/stop <id>
/help

---

## 🌐 Run API
python web/app.py

Endpoints:

Method	Endpoint	Purpose
GET	/	health
POST	/api/price	fetch price
POST	/api/track	start tracking

---

## 🛠 Stack

Python • Flask • BeautifulSoup • SQLite • Telegram Bot API
Docker • Kubernetes • Jenkins CI/CD

---

## 🗺 Roadmap

Scheduler (auto price checks)

Email alerts

Price history charts

Multi-store support

---

## 👨‍💻 Author

Ajeet Singh — DevOps & Platform Engineering
https://github.com/singhajeet79

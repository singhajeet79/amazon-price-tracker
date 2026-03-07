![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/API-Flask-green)
![Telegram](https://img.shields.io/badge/Bot-Telegram-blue)
![License](https://img.shields.io/badge/License-MIT-lightgrey)
![Status](https://img.shields.io/badge/Status-MVP-orange)

# 📉 PricePulse — Amazon Price Tracker

A Telegram-powered Amazon price tracker built with a modular backend architecture and DevOps-ready deployment design.
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

## ⚡ Quick Start

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

## 🎬 Demo

---

## ✅ Architecture Diagram
User → Telegram → Flask API → Service → Scraper → DB

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

## 🚧 Status
✅ MVP Complete  

---

## 🚧 Scheduler (Next)  
⬜ Cloud Deployment

---

## 👨‍💻 Author
Ajeet Singh — DevOps & Platform Engineering
https://github.com/singhajeet79

---

📜 License

MIT License

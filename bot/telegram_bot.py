import sys
from pathlib import Path
import asyncio

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from tracker.service import (
    track_product,
    list_user_trackers,
    stop_tracker
)
from tracker.scraper import ScrapingError

BOT_TOKEN = "7836139594:AAEzZ11-lpseNqos4Y-UhpxZxyrg0d4PF2Q"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "Welcome to PricePulseBot!\n\n"
        "Use:\n"
        "/track <amazon_url> <target_price>\n\n"
        "Example:\n"
        "/track https://www.amazon.in/dp/B0FLJY793G 16000"
    )


async def track(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args

        if len(args) != 2:
            await update.effective_message.reply_text(
                "Usage:\n/track <url> <target_price>"
            )
            return

        url = args[0]
        target_price = float(args[1])
        chat_id = str(update.effective_chat.id)

        result = track_product(
            url=url,
            target_price=target_price,
            channel="telegram",
            contact=chat_id,
        )

        await update.effective_message.reply_text(
            f"Tracking started!\n\n"
            f"{result['title']}\n"
            f"Current Price: {result['price']}\n"
            f"Alert at: {target_price}"
        )

    except ScrapingError as e:
        await update.effective_message.reply_text(f"Error: {str(e)}")
    except Exception as e:
        await update.effective_message.reply_text(f"Unexpected error: {str(e)}")


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "/track <url> <price>  - Track product\n"
        "/list               - Show active trackers\n"
        "/stop <id>          - Stop tracker\n"
        "/help               - Show commands"
    )


async def list_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    trackers = list_user_trackers(chat_id)

    if not trackers:
        await update.effective_message.reply_text("No active trackers.")
        return

    msg = "Your Trackers:\n\n"
    for t_id, title, price, target in trackers:
        msg += f"{t_id}. {title}\n   Current: {price}\n   Target: {target}\n\n"

    await update.effective_message.reply_text(msg)


async def stop_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.effective_message.reply_text("Usage: /stop <id>")
        return

    tracker_id = int(context.args[0])
    stop_tracker(tracker_id)
    await update.effective_message.reply_text("Tracker stopped.")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("track", track))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("list", list_cmd))
    app.add_handler(CommandHandler("stop", stop_cmd))

    print("Telegram bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()

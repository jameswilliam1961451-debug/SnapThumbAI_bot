import os
import logging
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Setup Logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!", 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting Flask on port {port}")
    app.run(host='0.0.0.0', port=port)

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Start command received from user!")
    await update.message.reply_text("✅ Bot is working! Send me a photo.")

async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Message received!")
    await update.message.reply_text("I'm online and receiving your messages!")

def main():
    if not TOKEN:
        logger.error("CRITICAL ERROR: BOT_TOKEN is missing from Environment Variables!")
        return

    # Start Flask to keep Render happy
    Thread(target=run_flask, daemon=True).start()

    # Start Bot
    logger.info("Initializing Telegram Bot...")
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ALL, handle_all))
    
    logger.info("Bot is now polling Telegram for messages...")
    application.run_polling()

if __name__ == '__main__':
    main()

# app.py - Complete working example
import os
import logging
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Flask app for Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

# Bot setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = "🎨 **ClickMagic AI is Online!**\nSend me a photo and a title to start"
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

def run_bot():
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    
    if not TOKEN:
        logger.error("No TELEGRAM_TOKEN found!")
        return

    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    
    logger.info("--- CLICKMAGIC AI STARTING ---")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    # Start bot in background thread
    Thread(target=run_bot).start()
    
    # Start Flask server for Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

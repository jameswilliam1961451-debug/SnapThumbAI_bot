import os
import logging
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Setup Logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(name)

# Flask App for Render Health Check
app = Flask(name)

@app.route('/')
def home():
    return "Bot is alive!", 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Telegram Bot Logic
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎨 ClickMagic AI is Online!\nSend me a photo and a title to start.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Got it! I'm working on your thumbnail... 🚀")

def main():
    if not TOKEN:
        logger.error("BOT_TOKEN environment variable is missing!")
        return

    # Start Flask in a background thread
    Thread(target=run_flask, daemon=True).start()

    # Start Telegram Bot
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ALL, handle_message))
    
    logger.info("Bot is starting...")
    application.run_polling()

if name == 'main':
    main()

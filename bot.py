import os
import logging
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# 1. SETUP LOGGING
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(name)

# 2. FLASK SERVER (Satisfies Render's Port Health Check)
server = Flask(name)

@server.route('/')
def index():
    return "Bot is alive!", 200

# 3. TELEGRAM BOT LOGIC
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎨 ClickMagic AI is Online!\nSend me a photo and a title to start.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Got it! I'm working on your thumbnail... 🚀")

async def main():
    # Setup Telegram Application
    if not TOKEN:
        logger.error("BOT_TOKEN is missing!")
        return

    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ALL, handle_message))

    # This starts the bot polling
    async with application:
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        
        # This keeps the bot running forever
        logger.info("Bot is polling...")
        
        # Start Flask in the background using a simple runner
        # Render needs this to see the "Port" is active
        from werkzeug.serving import run_simple
        port = int(os.environ.get("PORT", 8080))
        
        # We run the flask server in a loop to keep the process alive
        run_simple('0.0.0.0', port, server)

if name == 'main':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")

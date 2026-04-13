import os
import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Updated welcome message
    welcome_text = "🎨 **ClickMagic AI is Online!**\nSend me a photo and a title to start"
    
    # Using parse_mode='Markdown' so the bold text renders correctly
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def main():
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    
    if not TOKEN:
        logger.error("No TELEGRAM_TOKEN found in Environment Variables!")
        return

    # Build the application
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Add handler for the /start command
    application.add_handler(CommandHandler("start", start))
    
    logger.info("--- CLICKMAGIC AI STARTING ---")
    
    # Running the bot in an async context for Python 3.14 compatibility
    async with application:
        await application.initialize()
        await application.start()
        await application.updater.start_polling(drop_pending_updates=True)
        
        # Keep the background worker alive
        while True:
            await asyncio.sleep(3600)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")

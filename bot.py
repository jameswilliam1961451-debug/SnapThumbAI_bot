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

def main():
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    
    if not TOKEN:
        logger.error("No TELEGRAM_TOKEN found in Environment Variables!")
        return

    # Build the application
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Add handler for the /start command
    application.add_handler(CommandHandler("start", start))
    
    logger.info("--- CLICKMAGIC AI STARTING ---")
    
    # Run the bot - this is the correct way for production
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()

import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Get Token from Render Environment Variable
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎨 Welcome to ClickMagic AI!\n\n"
        "Send me a photo of yourself or your subject, and I'll turn it into a high-CTR YouTube thumbnail."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # This is where you would add your AI Image Generation logic
    user_text = update.message.text
    await update.message.reply_text(f"I received your title: '{user_text}'. Generating your thumbnail now... (Processing AI)")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Photo received! Now, please send the Title you want on the thumbnail.")

if name == 'main':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot is running...")
    app.run_polling()

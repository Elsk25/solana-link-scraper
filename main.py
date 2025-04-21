import logging
import re
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Regex pattern to detect solana token addresses in links
token_pattern = re.compile(r'(?:https?://\S*/token/)?([1-9A-HJ-NP-Za-km-z]{32,44})')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    text = update.message.text
    matches = token_pattern.findall(text)

    if matches:
        for token in matches:
            reply = f"Solana token address detected: {token}"
            await update.message.reply_text(reply)

if __name__ == '__main__':
    TOKEN = os.getenv("BOT_TOKEN")

    if not TOKEN:
        raise ValueError("BOT_TOKEN environment variable is required")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot is running...")
    app.run_polling()

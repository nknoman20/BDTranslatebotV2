import os
import logging
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from googletrans import Translator

# Logging চালু
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

translator = Translator()

def translate(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    # Detect language
    detected = translator.detect(text).lang
    # Decide target: ইংরিশ হলে বাংলায়, না হলে ইংরেজিতে
    target = 'bn' if detected == 'en' else 'en'
    try:
        translated = translator.translate(text, dest=target).text
        update.message.reply_text(f"🔄 {translated}")
    except Exception as e:
        logger.error(f"Translation error: {e}")
        update.message.reply_text("❌ অনুবাদ করতে পারছি না, পরে চেষ্টা করুন।")

def main():
    # BOT_TOKEN environment variable থেকে পড়বে
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        raise ValueError("BOT_TOKEN environment variable সেট করুন।")

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, translate))

    logger.info("Bot is starting...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

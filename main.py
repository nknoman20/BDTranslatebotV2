import os
import logging
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, MessageHandler, Filters, CallbackContext
from googletrans import Translator

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
app = Flask(__name__)
translator = Translator()

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# অনুবাদ ফাংশন
def translate(update: Update, context: CallbackContext):
    text = update.message.text
    detected = translator.detect(text).lang
    target = 'bn' if detected == 'en' else 'en'

    try:
        translated = translator.translate(text, dest=target).text
        update.message.reply_text(f"🔄 {translated}")
    except Exception as e:
        logger.error(f"Translation error: {e}")
        update.message.reply_text("❌ অনুবাদ করতে পারছি না।")

# Webhook হ্যান্ডলিং
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK", 200

@app.route('/')
def home():
    return "BD Translate Bot is Running!", 200

if __name__ == "__main__":
    from telegram.ext import Dispatcher
    dispatcher = Dispatcher(bot, None, use_context=True)
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, translate))

    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)

import os
import logging
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, Filters
from googletrans import Translator

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# টোকেন পড়ুন
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable সেট থাকে নাই!")

bot = Bot(token=TOKEN)
app = Flask(__name__)
translator = Translator()

# Dispatcher তৈরি
dispatcher = Dispatcher(bot, None, use_context=True)
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, 
                                     lambda update, ctx: update.message.reply_text(translator.translate(update.message.text, dest='bn' if translator.detect(update.message.text).lang == 'en' else 'en').text)
                                    ))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK", 200

@app.route("/", methods=["GET"])
def index():
    return "BD Translate Bot is live!", 200

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    logger.info("Starting Flask server...")
    app.run(host="0.0.0.0", port=PORT)

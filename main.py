import os
import logging
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from googletrans import Translator

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# টোকেন environment থেকে
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable সেট থাকে নাই!")

# Flask + Bot init
bot = Bot(token=TOKEN)
app = Flask(__name__)
translator = Translator()

# Dispatcher তৈরি
dispatcher = Dispatcher(bot, None, use_context=True)

# ✅ সাধারণ মেসেজের জন্য অনুবাদ
def handle_message(update, context):
    text = update.message.text
    lang = translator.detect(text).lang
    dest_lang = 'bn' if lang == 'en' else 'en'
    try:
        translated = translator.translate(text, dest=dest_lang).text
        update.message.reply_text(f" {translated}")
    except Exception as e:
        update.message.reply_text("❌ Translation failed.")
        logger.error(f"Translation error: {e}")

# ✅ /translate command এর জন্য handler
def translate_command(update, context):
    if not context.args:
        update.message.reply_text("⚠️ দয়া করে /translate এর পরে কিছু লিখুন।\nউদাহরণ: `/translate Hello`", parse_mode="Markdown")
        return
    text = ' '.join(context.args)
    lang = translator.detect(text).lang
    dest_lang = 'bn' if lang == 'en' else 'en'
    try:
        translated = translator.translate(text, dest=dest_lang).text
        update.message.reply_text(f"🔁 {translated}")
    except Exception as e:
        update.message.reply_text("❌ Translation failed.")
        logger.error(f"Command translation error: {e}")

# Handlers যুক্ত করা
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
dispatcher.add_handler(CommandHandler("translate", translate_command))

# Webhook endpoint → changed here to root '/'
@app.route("/", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK", 200

# Status route
@app.route("/", methods=["GET"])
def index():
    return "BD Translate Bot is live!", 200

# Run server
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    logger.info("Starting Flask server...")
    app.run(host="0.0.0.0", port=PORT)

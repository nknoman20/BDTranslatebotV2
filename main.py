import os
import logging
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from deep_translator import GoogleTranslator
from queue import Queue

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Token & Bot Init
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable সেট নাই!")
bot = Bot(token=TOKEN)
app = Flask(__name__)

# Dispatcher
update_queue = Queue()
dispatcher = Dispatcher(bot, update_queue, workers=4, use_context=True)

# Handlers
def start(update, context):
    update.message.reply_text("👋 স্বাগতম! আপনি যেকোনো টেক্সট পাঠান, আমি বাংলায় বা ইংরেজিতে অনুবাদ করে দিব।")

def handle_message(update, context):
    text = update.message.text
    try:
        # detect language and translate
        target_lang = 'bn' if GoogleTranslator(source='auto', target='bn').translate(text) != text else 'en'
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        update.message.reply_text(translated)
    except Exception as e:
        update.message.reply_text("❌ অনুবাদ ব্যর্থ হয়েছে।")
        logger.error(f"Translation error: {e}")

def translate_command(update, context):
    if not context.args:
        update.message.reply_text("⚠️ দয়া করে /translate এর পরে কিছু লিখুন।\nউদাহরণ: `/translate Hello`", parse_mode="Markdown")
        return
    text = ' '.join(context.args)
    try:
        target_lang = 'bn' if GoogleTranslator(source='auto', target='bn').translate(text) != text else 'en'
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        update.message.reply_text(f"🔁 {translated}")
    except Exception as e:
        update.message.reply_text("❌ অনুবাদ ব্যর্থ হয়েছে।")
        logger.error(f"Command translation error: {e}")

# Handlers Register
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("translate", translate_command))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Webhook route
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK", 200

# Health route
@app.route("/", methods=["GET"])
def index():
    return "BD Translate Bot is live!", 200

# Run
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    logger.info("Starting Flask server...")
    app.run(host="0.0.0.0", port=PORT)

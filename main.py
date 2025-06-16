from flask import Flask, request
import telegram
from telegram.ext import Dispatcher, MessageHandler, Filters
from googletrans import Translator
import os

TOKEN = os.environ.get("BOT_TOKEN")
bot = telegram.Bot(token=TOKEN)

translator = Translator()

app = Flask(__name__)

@app.route('/')
def home():
    return '🤖 Bot is alive.'

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dp.process_update(update)
    return 'ok'

def translate(update, context):
    text = update.message.text
    detected = translator.detect(text).lang
    dest = 'bn' if detected == 'en' else 'en'
    translated = translator.translate(text, dest=dest).text
    update.message.reply_text(f"🔄 {translated}")

dp = Dispatcher(bot, None, workers=0)
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, translate))

from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from telegram import Update
from googletrans import Translator
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
translator = Translator()

def translate(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    detected = translator.detect(text).lang
    target = 'bn' if detected == 'en' else 'en'
    translated = translator.translate(text, dest=target).text
    update.message.reply_text(f"🔄 {translated}")

TOKEN = "7753604536:AAG6h9U_XGICIB9vmo5x8slt6XtmhLPnouo"

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, translate))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

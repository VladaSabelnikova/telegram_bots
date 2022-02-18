import os

import requests
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, \
    ConversationHandler

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
address = 'https://api.mymemory.translated.net/get?q={0}!&langpair={1}'
langpair = ''


def start(update, context):
    reply_keyboard = [['ru|en', 'en|ru']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    update.message.reply_text(
        'Привет! А Елена Александровна была не права. Не веришь?'
        '\nС какого на какой язык мне переводить?',
        reply_markup=markup
    )
    return 1


def get_langpair(update, context):
    global langpair
    langpair = update.message.text
    update.message.reply_text('Хорошо, а что мне переводить?')
    return 2


def translator(update, context):
    text = update.message.text
    addr = address.format(text, langpair)

    response = requests.get(addr)
    if response.status_code == 200:
        json_response = response.json()
        result = json_response['responseData']['translatedText']
        update.message.reply_text(result)

    else:
        update.message.reply_text('К сожалению сервер упал. Зайдите позже')

    return 2


def stop(update, context):
    update.message.reply_text('Всего доброго')


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(Filters.text, get_langpair)],
            2: [MessageHandler(Filters.text, translator)],
        },

        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

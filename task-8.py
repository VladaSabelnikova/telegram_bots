import json
import os
import random
from pathlib import Path

from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, \
    ConversationHandler

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
response = ''


def json_get(update, context):
    global response
    json_file = Path(
        'D:/work/yandex_liceum/2_year/part_2/bots/file.json'
    ).read_text(encoding='utf-8')

    data = json.loads(json_file)
    test = random.choice(data['test'])

    question = test['question']
    response = test['response']

    update.message.reply_text(question)

    return 1


def check(update, context):
    resp = update.message.text
    if resp == response:
        update.message.reply_text('Отгадали!')
    else:
        update.message.reply_text(f'Лох, правильный ответ {response}!')

    json_get(update, context)


def stop(update, context):
    update.message.reply_text('Пока!')
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', json_get)],
        states={
            1: [MessageHandler(Filters.text, check)],
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

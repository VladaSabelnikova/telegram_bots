import os
import time

from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')


def current_time(update, context):
    date = time.asctime().split()
    update.message.reply_text(
        f'Сейчас {date[3]}'
    )


def current_date(update, context):
    date = time.asctime().split()
    update.message.reply_text(
        f'Сегодня у нас {" ".join(date[1:3])} {date[-1]}'
    )


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    time_handler = CommandHandler('time', current_time)
    date_handler = CommandHandler('date', current_date)

    dp.add_handler(time_handler)
    dp.add_handler(date_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

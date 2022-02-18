import os

from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, \
    ConversationHandler

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')


def start(update, context):
    update.message.reply_text(
        'Вас приветствует Бот-экскурсовод!\n'
        'Вы можете проследовать в зал № 1\n'
        'Для этого скажите "перейти"'
    )
    return 1


def hall_1(update, context):
    update.message.reply_text(
        'Добро пожаловать в зал 1! Пожалуйста, сдайте верхнюю одежду в гардероб!'
        'Вы можете проследовать в зал № 2\n'
        'Для этого скажите "перейти"'
    )

    update.message.reply_text(
        'В данном зале представлены древние фрески.'
    )

    return 2


def hall_2(update, context):
    update.message.reply_text(
        'Добро пожаловать в зал 2! Пожалуйста, сдайте верхнюю одежду в гардероб!'
        'Вы можете проследовать в зал № 3\n'
        'Для этого скажите "перейти"'
    )

    update.message.reply_text(
        'В данном зале представлены доспехи.'
    )

    return 3


def hall_3(update, context):
    update.message.reply_text(
        'Добро пожаловать в зал 3! Пожалуйста, сдайте верхнюю одежду в гардероб!'
        'Вы можете проследовать в зал № 4 или же в зал № 1\n'
        'Для этого скажите либо "4", либо "1"'
    )

    update.message.reply_text(
        'В данном зале представлены вазы.'
    )

    return 5


def hall_4(update, context):
    update.message.reply_text(
        'Добро пожаловать в зал 4! Пожалуйста, сдайте верхнюю одежду в гардероб!'
        'Вы можете проследовать в зал № 1\n'
        'Для этого скажите "перейти"'
    )

    update.message.reply_text(
        'В данном зале представлены красивые картины.'
    )

    return 1


def check(update, context):
    response = update.message.text
    if response == '1':
        hall_1(update, context)
    elif response == '4':
        hall_4(update, context)


def stop(update, context):
    update.message.reply_text(
        'Всего доброго, не забудьте забрать верхнюю одежду в гардеробе!'
    )


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(Filters.text, hall_1)],
            2: [MessageHandler(Filters.text, hall_2)],
            3: [MessageHandler(Filters.text, hall_3)],
            4: [MessageHandler(Filters.text, hall_4)],
            5: [MessageHandler(Filters.text, check)],
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

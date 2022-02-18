import os

from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler, \
    CommandHandler

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')


def stop(update, context):
    return ConversationHandler.END


def start(update, context):
    update.message.reply_text(
        "Привет. Пройдите небольшой опрос, пожалуйста!\n"
        "Вы можете прервать опрос, послав команду /stop.\n"
        "В каком городе вы живёте?")
    return 1


def first_response(update, context):
    locality = update.message.text
    if locality == 'skip':
        return 3
    if locality == 'хорошая':
        second_response(update, context)
    else:
        update.message.reply_text(
            "Какая погода в городе {locality}?".format(**locals()))
        return 2


def first_response_window(update, context):
    update.message.reply_text(
        "Какая погода у вас за окном?"
    )


def second_response(update, context):
    weather = update.message.text
    print(weather)
    update.message.reply_text("Спасибо за участие в опросе! Всего доброго!")
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(Filters.text, first_response)],
            2: [MessageHandler(Filters.text, second_response)],
            3: [MessageHandler(Filters.text, first_response_window)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(CommandHandler('skip', first_response_window))
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

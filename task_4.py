import os
import random

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, \
    ConversationHandler

from task_3 import remove_job_if_exists

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')


def start(update, context):
    reply_keyboard = [['/dice', '/timer']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    update.message.reply_text(
        'Чего вы хотите?',
        reply_markup=markup
    )
    return 1


def game(update, context):
    response = update.message.text

    if response == 'кинуть один шестигранный кубик':
        update.message.reply_text('Кидаю!')
        update.message.reply_text(f'{random.randrange(1, 6, 1)}')

    elif response == 'кинуть 2 шестигранных кубика одновременно':
        update.message.reply_text('Кидаю!')
        update.message.reply_text(
            f'{random.randrange(1, 6, 1)} и {random.randrange(1, 6, 1)}'
        )

    elif response == 'кинуть 20-гранный кубик':
        update.message.reply_text('Кидаю!')
        update.message.reply_text(f'{random.randrange(1, 20, 1)}')

    elif response == 'вернуться назад':
        start(update, context)
        return ConversationHandler.END


def task(context):
    job = context.job
    context.bot.send_message(job.context, text='Вернулся!')


def timer(update, context):
    seconds = None

    response = update.message.text
    chat_id = update.message.chat_id

    if response == '30 секунд':
        seconds = 30

    elif response == '1 минута':
        seconds = 60

    elif response == '5 минут':
        seconds = 300

    elif response == '1 секунда':
        seconds = 1

    elif response == 'вернуться назад':
        return ConversationHandler.END

    if seconds:

        job_removed = remove_job_if_exists(
            str(chat_id),
            context
        )
        context.job_queue.run_once(
            task,
            seconds,
            context=chat_id,
            name=str(chat_id)
        )
        text = f'Вернусь через {seconds} секунд!'
        if job_removed:
            text += ' Старая задача удалена.'
        update.message.reply_text(text)


def choice(update, context):
    response = update.message.text

    update.message.reply_text(
        'Хорошо!'
    )

    game(update, context)
    timer(update, context)

    if response == '/dice':
        reply_keyboard = [
            [
                'кинуть один шестигранный кубик',
                'кинуть 2 шестигранных кубика одновременно'
            ],
            [
                'кинуть 20-гранный кубик',
                'вернуться назад'
            ]
        ]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

        update.message.reply_text(
            'Чего будем кидать?',
            reply_markup=markup
        )

    elif response == '/timer':
        reply_keyboard = [
            [
                '30 секунд',
                '1 минута',
                '1 секунда'
            ],
            [
                '5 минут',
                'вернуться назад'
            ]
        ]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

        update.message.reply_text(
            'Сколько мне ждать?',
            reply_markup=markup
        )


def stop(update, context):
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(Filters.text, choice)],
            2: [MessageHandler(Filters.text, game)],
            4: [MessageHandler(Filters.text, timer)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

import os

from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, \
    ConversationHandler

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

VERSE = (
    'Суровый Дант не презирал сонета;',
    'В нем жар любви Петрарка изливал;',
    'Игру его любил творец Макбета;',
    'Им скорбну мысль Камоэнс облекал.',

    'И в наши дни пленяет он поэта:',
    'Вордсворт его орудием избрал,',
    'Когда вдали от суетного света',
    'Природы он рисует идеал.',

    'Под сенью гор Тавриды отдаленной',
    'Певец Литвы в размер его стесненный',
    'Свои мечты мгновенно заключал.',

    'У нас еще его не знали девы,',
    'Как для него уж Дельвиг забывал',
    'Гекзаметра священные напевы.'
)

index = 0


def start(update, context):
    update.message.reply_text(
        'Вас приветствует Бот-литератор!\n'
    )

    update.message.reply_text(
        f'Первая строка:\n'
        f'{VERSE[index]}'
    )

    return 1


def game(update, context):
    global index
    response = update.message.text
    if response == VERSE[min(index + 1, len(VERSE))]:
        update.message.reply_text(f'{VERSE[min(index + 2, len(VERSE))]}')
        index += 2
    else:
        update.message.reply_text('Нет, не так')
        update.message.reply_text(
            f'Правильно так:\n'
            f'{VERSE[min(index + 1, len(VERSE))]}'
        )
    if index == len(VERSE):
        update.message.reply_text('Выражаю свою радость!')


def stop(update, context):
    update.message.reply_text(
        'Всего доброго'
    )
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    start_handler = CommandHandler('start', start)
    stop_handler = CommandHandler('stop', stop)
    text = MessageHandler(Filters.text, game)

    dp.add_handler(start_handler)
    dp.add_handler(stop_handler)
    dp.add_handler(text)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

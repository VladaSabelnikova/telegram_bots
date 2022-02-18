import os

import requests as requests
from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, Filters


load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
API_KEY = os.getenv('API_KEY')


def geocoder(update, context):
    geocoder_uri = geocoder_request_template = "http://geocode-maps.yandex.ru/1.x/"
    response = requests.get(geocoder_uri, params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "format": "json",
        "geocode": update.message.text
    })

    if not response.json()["response"]["GeoObjectCollection"]["featureMember"]:
        update.message.reply_text(
            'Ничего не найдено, возможно вы неверно ввели название локации'
        )

    else:
        toponym = response.json()["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]

        ll, spn = ','.join(toponym['Point']['pos'].split()), '0.3,0.3'

        static_api_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l=map"

        context.bot.send_photo(
            update.message.chat_id,
            static_api_request,
            caption="Нашёл:"
        )


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    photo_handler = MessageHandler(Filters.text, geocoder)

    dp.add_handler(photo_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

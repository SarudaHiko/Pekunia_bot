import json
import requests
import telebot
from loguru import logger
import time
from config import val, TOKEN

bot = telebot.TeleBot(TOKEN)

logger.add('logs.log', format='{level} | {message}', level='INFO', rotation='1 MB', compression='zip')


class APIException(Exception):
    pass


class Converter:
    @bot.message_handler()
    def photo_replay(message: telebot.types.Message):
        global name
        name = message.from_user.full_name

    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        try:
            quote_ticker = val[quote]
        except KeyError:
            raise APIException(f'Что-то не так с валютой "{quote}", проверьте написание и попробуйте снова 😉')
            logger.error(f'{name=} | {time.asctime()}')

        try:
            base_ticker = val[base]
        except KeyError:
            raise APIException(f'Что-то не так с валютой "{base}", проверьте написание и попробуйте снова 😉')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Что-то не так с количеством, проверьте написание "{amount}" и попробуйте снова 😉')

        url = f'https://api.exchangerate.host/convert?from={quote_ticker}&to={base_ticker}&amount={amount}'
        r = requests.get(url)
        total_base = json.loads(r.content)['result']

        return total_base

import telebot
import json
import requests
from config import val, TOKEN

bot = telebot.TeleBot(TOKEN)


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        try:
            quote_ticker = val[quote]
        except KeyError:
            raise APIException(f'Что-то не так с валютой "{quote}", проверьте написание и попробуйте снова 😉')

        try:
            base_ticker = val[base]
        except KeyError:
            raise APIException(f'Что-то не так с валютой "{base}", проверьте написание и попробуйте снова 😉')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(
                f'Что-то не так с количеством, проверьте написание "{amount}" и попробуйте снова 😉')

        url = f'https://api.exchangerate.host/convert?from={quote_ticker}&to={base_ticker}&amount={amount}'
        r = requests.get(url)
        total_base = json.loads(r.content)['result']

        return total_base

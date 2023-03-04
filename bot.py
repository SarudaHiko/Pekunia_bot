import telebot
from extensions import APIException, Converter
from config import TOKEN, val, cur, crip


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    bot.reply_to(message, f"Добро пожаловать, {message.chat.first_name}!\n"
                          'Этот бот конвертирует выбранную вами валюту и криптовалюту.\n'
                          f"Чтобы узнать как работать с ботом, нажмите /help")


@bot.message_handler(commands=['help'])
def helper(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Чтобы воспользоваться конвертором, введите данные в формате:\n'
                                      '{первая валюта(откуда)}, {вторая валюта(куда)}, {количество}\n'
                                      'Наличие запятых между валютами ОБЯЗАТЕЛЬНО ввиду разности валютных названий\n'
                                      'Пример правильных запросов: "доллар, рубль, 50" или "турецкая лира, йена, 100"\n'
                                      'Чтобы увидеть список валют, нажмите /values\n'
                                      'Или /cripto, чтобы увидеть список доступных криптовалют')


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:\n'
    for key in sorted(cur.keys()):
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(commands=['cripto'])
def values(message: telebot.types.Message):
    text = 'Доступные криптовалюты:\n'
    for key in crip.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


# @bot.message_handler(commands=['stop'])
# def stop(message):
#     bot.stop_bot()


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        value = message.text.lower().split(', ')

        if len(value) != 3:
            raise APIException('Введено не 3 параметра или где-то опечатка 😞')

        quote, base, amount = value
        total_base = Converter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Будьте внимательнее пожалуйста ☺️\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Упс, что-то пошло не так 🥺\n{e}')
    else:
        text = f'{amount} {val[quote]} в {val[base]} - {total_base}'
        bot.reply_to(message, text)


# @bot.message_handler(content_types=['text'])
# def echo_reply(message: telebot.types.Message):
#     bot.reply_to(message, message.text)


@bot.message_handler(content_types=['voice'])
def voice_reply(message: telebot.types.Message):
    bot.reply_to(message, 'Пока не могу слушать голосовые...\n Но уверен, что у вас замечательный голос)))')


@bot.message_handler(content_types=['photo'])
def photo_replay(message: telebot.types.Message):
    bot.reply_to(message, 'Если бы я знал, что на этой картинке, может быть мне и понравилось бы)))')


if __name__ == '__main__':
    bot.polling(none_stop=True)

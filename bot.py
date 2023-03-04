import telebot
from loguru import logger
import time
from extensions import APIException, Converter
from config import TOKEN, val, cur, cryp


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def starter(message: telebot.types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    logger.add('logs.log', format='{level} | {time} | {message}', level='INFO')
    logger.info(f'{user_id=} | {user_name=} | {time.asctime()}')

    bot.reply_to(message, f"Добро пожаловать, {message.chat.first_name}!\n"
                          'Этот бот конвертирует выбранную вами валюту и криптовалюту.\n'
                          "Чтобы узнать как работать с ботом, нажмите /help")


@bot.message_handler(commands=['help'])
def helper(message: telebot.types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    logger.add('logs.log', format='{level} | {time} | {message}', level='INFO')
    logger.info(f'{user_id=} | {user_name=} | {time.asctime()}')

    bot.send_message(message.chat.id, 'Чтобы воспользоваться конвертором, введите данные в формате:\n'
                                      '{первая валюта(откуда)}, {вторая валюта(куда)}, {количество}\n'
                                      'Наличие запятых между валютами ОБЯЗАТЕЛЬНО ввиду разности валютных названий\n'
                                      'Пример правильных запросов: "доллар, рубль, 50" или "турецкая лира, йена, 100"\n'
                                      'Чтобы увидеть список валют, нажмите /values\n'
                                      'Или /crypto, чтобы увидеть список доступных криптовалют')


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    logger.add('logs.log', format='{level} | {time} | {message}', level='INFO')
    logger.info(f'{user_id=} | {user_name=} | {time.asctime()}')
    
    text = 'Доступные валюты:\n'
    for key in sorted(cur.keys()):
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(commands=['crypto'])
def crypto(message: telebot.types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name
    logger.add('logs.log', format='{level} | {time} | {message}', level='INFO')
    logger.info(f'{user_id=} | {user_name=} | {time.asctime()}')
    
    text = 'Доступные криптовалюты:\n'
    for key in cryp.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    global reply
    try:
        value = message.text.lower().split(', ')

        if len(value) != 3:
            raise APIException('Введено не 3 параметра или где-то опечатка 😞')

        quote, base, amount = value
        total_base = Converter.get_price(quote, base, amount)

        if total_base is None:
            raise APIException('Вероятнее всего, не получится конвертировать данные валюты. Приносим извинения')

    except APIException as e:
        bot.reply_to(message, f'Что-то написано неправильно, проверьте, пожалуйста ☺️\n\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Упс, что-то пошло не так 🥺\n{e}')
    else:
        reply = f'{amount} {val[quote]} в {val[base]} - {total_base}'
        bot.reply_to(message, reply)

    user_name = message.from_user.full_name
    logger.add('logs.log', format='{level} | {time} | {message}', level='INFO')
    logger.info(f'{user_name=} | {reply=} | {time.asctime()}')


@bot.message_handler(content_types=['voice'])
def voice_reply(message: telebot.types.Message):
    bot.reply_to(message, 'Пока не могу слушать голосовые...\n Но уверен, что у вас замечательный голос)))')


@bot.message_handler(content_types=['photo'])
def photo_replay(message: telebot.types.Message):
    bot.reply_to(message, 'Если бы я знал, что на этой картинке, может быть мне и понравилось бы)))')


if __name__ == '__main__':
    bot.polling(none_stop=True)

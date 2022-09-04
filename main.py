import telebot
import requests
from telebot import types
from bs4 import BeautifulSoup as bs
from config import TOKEN


bot = telebot.TeleBot(TOKEN)

sait_goroskop = requests.get('https://74.ru/horoscope/daily/')
soup = bs(sait_goroskop.text, 'lxml')
a = soup.find('section', class_='IjM3t')
b = [i for i in a]
b = b[2:]
predskazania = []
for i in b:
    predskazania.append(str(i)[str(i).rfind('KUbeq') + 12:-22])
spisokZnakov = ['ОВЕН', 'ТЕЛЕЦ', 'БЛИЗНЕЦЫ', 'РАК', 'ЛЕВ', 'ДЕВА', 'ВЕСЫ', 'СКОРПИОН', 'СТРЕЛЕЦ', 'КОЗЕРОГ', 'ВОДОЛЕЙ', 'РЫБЫ']

gotoviePredsakzania = dict(zip(spisokZnakov, predskazania))
print(gotoviePredsakzania)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Хочу прогноз!")
    btn2 = types.KeyboardButton("❓ Контакты разработчика")
    btn3 = types.KeyboardButton("❓ Информация о прогнозах")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id,
                     "Привет, {0.first_name}! Я - бот гороскоп, могу прислать тебе прогноз по знаку зодиака на сегодня!".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "Хочу прогноз!":
        bot.send_message(message.chat.id, text=f"Хорошо! Напишите свой знак зодиака:")
    elif message.text == "❓ Контакты разработчика":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Контакт в телеграме")
        button2 = types.KeyboardButton("Гитхаб")
        button3 = types.KeyboardButton("Вернуться обратно")
        markup.add(button1)
        markup.add(button2)
        markup.add(button3)
        bot.send_message(message.chat.id, text="Какой именно контакт вам нужен?", reply_markup=markup)

    elif message.text == "Гитхаб":
        bot.send_message(message.chat.id, text="https://github.com/Grasmurr")

    elif message.text == '❓ Информация о прогнозах':
        bot.send_message(message.chat.id, text ="Вся информация взята с сайта https://74.ru/")

    elif message.text.upper() in spisokZnakov:
        bot.send_message(message.chat.id, text=gotoviePredsakzania[message.text.upper()])


    elif message.text == "Контакт в телеграме":
        bot.send_message(message.chat.id, text="@Grasmurr")

    elif message.text == "Вернуться обратно":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Хочу прогноз!")
        btn2 = types.KeyboardButton("❓ Контакты разработчика")
        btn3 = types.KeyboardButton("❓ Информация о прогнозах")
        markup.add(btn1)
        markup.add(btn2)
        markup.add(btn3)
        bot.send_message(message.chat.id,
                         'Вы вернулись в главное меню!'.format(
                             message.from_user), reply_markup=markup)

    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")


bot.polling(none_stop=True, interval=0)

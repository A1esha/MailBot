import pymysql
import telebot
from telebot import types
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

# connection = pymysql.connect(host="localhost", port=3306, user="root", passwd="root", database="bot")
# cursor = connection.cursor()

# cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")

# sql = """INSERT INTO offers(NAME, CITY, DATEOF, TELEGRAM_ID)
#    VALUES ('Aliaksei', 'Bratisava', "10 мая", "@HEDGEH0G_1")"""
#
# try:
#    cursor.execute(sql)
#    connection.commit()
# except:
#    connection.rollback()

token = ""

bot = telebot.TeleBot(token)

flag = 0
# if flag = 1 - search, if flag = -1 - add to the db

info = {}

now = 1

el = []


def search(date):
    # sql = f"INSERT INTO package(NAME, CITY, TYPEOFPACK, DAY, TELEGRAM_ID) VALUES ('{info['name']}', '{info['city']}', '{info[date]}', '{info['telegramid']}"
    # print(sql)
    st = ''
    for i in el:
        if i['date'] >= date:
            print(i)
            st += str(i['telegramid'])
    return st


def add(date):
    el.append(date)
    # sql = f"INSERT INTO package(NAME, CITY, TYPEOFPACK, DAY, TELEGRAM_ID) VALUES ('{info['name']}', '{info['city']}', '{info[date]}', '{info['telegram.id}']}"


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton("Отправитель")
    btn2 = types.KeyboardButton("Перевозчик")
    markup.add(btn1, btn2)
    info['telegramid'] = message.from_user.username
    info['name'] = message.from_user.first_name
    bot.send_message(message.chat.id,
                     text="Здравствуйте, {0.first_name}! Выберете кто вы".format(message.from_user),
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    global flag
    global now
    if message.text == "Отправитель":
        flag = 1
        calendar, step = DetailedTelegramCalendar().build()
        bot.send_message(message.chat.id, f"Выберите год поиска", reply_markup=calendar)
    elif message.text == "Перевозчик":
        flag = -1
        calendar, step = DetailedTelegramCalendar().build()
        bot.send_message(message.chat.id, f"Выберите год ваше поездки", reply_markup=calendar)
    else:
        bot.send_message(message.chat.id, f"Чтобы начать работу ввредите /start")


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    result, key, step = DetailedTelegramCalendar().process(c.data)
    global flag
    if flag == 1:
        if not result and key:
            bot.edit_message_text(f"Выберите время, начиная с которого мы будет отслеживать перевозчиков", c.message.chat.id, c.message.message_id,
                                  reply_markup=key)
        elif result:
            text = search(result)
            st = "Nich"
            if len(text) == 0:
                bot.send_message(c.message.chat.id, text="К сожалению в заданный вами период на данный момент ни один перевозчик не едет. Попробуйте найти его позже")
            else:
                st = "Вот что удалось найти по вашему запросу"

            print(st)
            bot.edit_message_text(f"You selected @{text}", c.message.chat.id, c.message.message_id)
    else:
        if not result and key:
            bot.edit_message_text(f"Выберите время вашей поездки",
                                  c.message.chat.id, c.message.message_id, reply_markup=key)
        elif result:
            info['date'] = result
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Беларусь")
            btn2 = types.KeyboardButton("Словакия")
            markup.add(btn1, btn2)
            msg = bot.send_message(c.message.chat.id,
                             text="Выберите страну отправления(откуда едете)".format(c.from_user),
                             reply_markup=markup)
            bot.register_next_step_handler(msg, city1)


def city1(message):
    if message.text == 'Беларусь':
        info['country1'] = 'Беларусь'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Минск")
        btn2 = types.KeyboardButton("Гомель")
        btn3 = types.KeyboardButton("Витебск")
        btn4 = types.KeyboardButton("Могилев")
        btn5 = types.KeyboardButton("Брест")
        btn6 = types.KeyboardButton("Гродно")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        msg = bot.send_message(message.chat.id,
                               text="Выберите город отправления".format(message.from_user),
                               reply_markup=markup)
        bot.register_next_step_handler(msg, go_to_type)
    elif message.text == 'Словакия':
        info['country1'] = 'Словакия'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Братислава")
        btn2 = types.KeyboardButton("Нитра")
        btn3 = types.KeyboardButton("Кошице")
        markup.add(btn1, btn2, btn3)
        msg = bot.send_message(message.chat.id,
                               text="Выберите город отправления".format(message.from_user),
                               reply_markup=markup)
        bot.register_next_step_handler(msg, go_to_type)
    else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Беларусь")
            btn2 = types.KeyboardButton("Словакия")
            markup.add(btn1, btn2)
            msg = bot.send_message(message.chat.id,
                             text="Выберите страну отправления(откуда едете)".format(message.from_user),
                             reply_markup=markup)
            bot.register_next_step_handler(msg, city1)


def go_to_type(message):
    if message.text in ["Минск", "Гомель", "Гродно", "Витебск", "Могилев", "Брест"]:
        info['city1'] = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Словакия")
        markup.add(btn1)
        msg = bot.send_message(message.chat.id,
                               text="Выберите страну приезда".format(message.from_user),
                               reply_markup=markup)
        bot.register_next_step_handler(msg, city2)

    elif message.text in ['Братислава', 'Нитра', 'Кошице']:
        info['city1'] = message.text
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Беларусь")
        markup.add(btn1)
        msg = bot.send_message(message.chat.id,
                               text="Выберите страну приезда".format(message.from_user),
                               reply_markup=markup)
        bot.register_next_step_handler(msg, city2)
    else:
        if info['country1'] == 'Беларусь':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Минск")
            btn2 = types.KeyboardButton("Гомель")
            btn3 = types.KeyboardButton("Витебск")
            btn4 = types.KeyboardButton("Могилев")
            btn5 = types.KeyboardButton("Брест")
            btn6 = types.KeyboardButton("Гродно")
            markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
            msg = bot.send_message(message.chat.id,
                                   text="Выберите город отправления".format(message.from_user),
                                   reply_markup=markup)
            bot.register_next_step_handler(msg, go_to_type)
        elif info['country1'] == 'Словакия':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Братислава")
            btn2 = types.KeyboardButton("Кошице")
            btn3 = types.KeyboardButton("Нитра")
            markup.add(btn1, btn2, btn3)
            msg = bot.send_message(message.chat.id,
                                   text="Выберите город отправления".format(message.from_user),
                                   reply_markup=markup)
            bot.register_next_step_handler(msg, go_to_type)


def city2(message):
    if message.text == 'Словакия':
        info['country2'] = 'Словакия'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Братислава")
        btn2 = types.KeyboardButton("Нитра")
        btn3 = types.KeyboardButton("Кошице")
        markup.add(btn1, btn2, btn3)
        msg = bot.send_message(message.chat.id,
                               text="Выберите город приезда".format(message.from_user),
                               reply_markup=markup)
        bot.register_next_step_handler(msg, city_to)
    elif message.text == 'Беларусь':
        info['country2'] = 'Беларусь'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Минск")
        btn2 = types.KeyboardButton("Гомель")
        btn3 = types.KeyboardButton("Витебск")
        btn4 = types.KeyboardButton("Могилев")
        btn5 = types.KeyboardButton("Брест")
        btn6 = types.KeyboardButton("Гродно")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        msg = bot.send_message(message.chat.id,
                               text="Выберите город приезда".format(message.from_user),
                               reply_markup=markup)
        bot.register_next_step_handler(msg, city_to)


def city_to(message):
    if message.text in ["Минск", "Гомель", "Гродно", "Витебск", "Могилев", "Брест"]:
        info['city2'] = message.text
    elif message.text in ['Братислава', "Нитра", "Кошице"]:
        info['city2'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Документы")
    btn2 = types.KeyboardButton("Маленькие посылки")
    btn3 = types.KeyboardButton("Посылки среднего размера")
    btn4 = types.KeyboardButton("Большие посылки")
    markup.add(btn1, btn2, btn3, btn4)
    msg = bot.send_message(message.chat.id,
                           text="Выберите максимальный размер посылки, который Вы бы могли перевезти".format(message.from_user),
                           reply_markup=markup)
    bot.register_next_step_handler(msg, type_of_send)


def type_of_send(message):
    if message.text == "Документы":
        info['size'] = 0
    elif message.text == "Маленькие посылки":
        info['size'] = 1
    elif message.text == "Посылки среднего размера":
        info['size'] = 2
    elif message.text == "Большие посылки":
        info['size'] = 3
    text = ""
    if info['size'] == 0:
        text = "Документы"
    elif info['size'] == 1:
        text = "Маленьнике посылки"
    elif info['size'] == 2:
        text = "Посылки среднего размера"
    elif info['size'] == 3:
        text = "Большие посылки"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Все верно")
    btn2 = types.KeyboardButton("Хотел бы отредактировать некоторую информацию")
    markup.add(btn1, btn2)
    msg = bot.send_message(message.chat.id,
                     text=f"Ваши данные были обработаны. Проверьте их правильность\n: Ваше имя: {info['name']}\nВаш телеграмм: @{info['telegramid']}\nГород отправления: {info['city1']}\nГород прибытия: {info['city2']}\nДень отправления: {info['date']}\nТип посылок: {text}", reply_markup=markup)
    bot.register_next_step_handler(msg, true_or_false)


def true_or_false(message):
    if message.text == "Все верно":
        print(info)
        add(info)
        a = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, text="Ваши данные успешно добавлены. Спасибо за то, что готовы помочь", reply_markup=a)
    elif message.text == "Хотел бы отредактировать некоторую информацию":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Имя")
        btn2 = types.KeyboardButton("Город отправления")
        btn3 = types.KeyboardButton("Город прибытия")
        btn5 = types.KeyboardButton("Тип посылки")
        markup.add(btn1, btn2, btn3, btn5)
        msg = bot.send_message(message.chat.id,
                         text="Выберите данные, которые хотите исправить", reply_markup=markup)
        bot.register_next_step_handler(msg, fixed)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Все верно")
        btn2 = types.KeyboardButton("Хотел бы отредактировать некоторую информацию")
        markup.add(btn1, btn2)
        text = ""
        if info['size'] == 0:
            text = "Документы"
        elif info['size'] == 1:
            text = "Маленьнике посылки"
        elif info['size'] == 2:
            text = "Посылки среднего размера"
        elif info['size'] == 3:
            text = 'Большие посылки'
        msg = bot.send_message(message.chat.id,
                         text=f"Ваши данные были обработаны. Проверьте их правильность:\n Ваше имя: {info['name']}\nВаш телеграмм: @{info['telegramid']}\nГород отправления: {info['city1']}\nГород прибытия: {info['city2']}\nДень отправления: {info['date']}\nТип посылок: {text}",
                         reply_markup=markup)
        bot.register_next_step_handler(msg, true_or_false)


def fixed(message):
    if message.text == 'Имя':
        msg = bot.send_message(message.chat.id,
                         text="Введите Ваше имя")
        # bot.next_step_backend(msg, new_name)
        bot.register_next_step_handler(msg, new_name)
    elif message.text == 'Город отправления':
        if info['country1'] == 'Беларусь':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Минск")
            btn2 = types.KeyboardButton("Гомель")
            btn3 = types.KeyboardButton("Витебск")
            btn4 = types.KeyboardButton("Могилев")
            btn5 = types.KeyboardButton("Брест")
            btn6 = types.KeyboardButton("Гродно")
            markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
            msg = bot.send_message(message.chat.id,
                                   text="Выберите город отправления".format(message.from_user),
                                   reply_markup=markup)
            bot.register_next_step_handler(msg, from_city)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Братислава")
            btn2 = types.KeyboardButton("Нитра")
            btn3 = types.KeyboardButton("Кошице")
            markup.add(btn1, btn2, btn3)
            msg = bot.send_message(message.chat.id,
                                   text="Выберите город отправления".format(message.from_user),
                                   reply_markup=markup)
            bot.next_step_backend(msg, to_city)

    elif message.text == 'Город прибытия':
        if info['country1'] == 'Беларусь':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Минск")
            btn2 = types.KeyboardButton("Гомель")
            btn3 = types.KeyboardButton("Витебск")
            btn4 = types.KeyboardButton("Могилев")
            btn5 = types.KeyboardButton("Брест")
            btn6 = types.KeyboardButton("Гродно")
            markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
            msg = bot.send_message(message.chat.id,
                                   text="Выберите город прибытия".format(message.from_user),
                                   reply_markup=markup)
            bot.next_step_backend(msg, to_city)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Братислава")
            btn2 = types.KeyboardButton("Нитра")
            btn3 = types.KeyboardButton("Кошице")
            markup.add(btn1, btn2, btn3)
            msg = bot.send_message(message.chat.id,
                                   text="Выберите город отправления".format(message.from_user),
                                   reply_markup=markup)
            bot.next_step_backend(msg, to_city)
    elif message.text == 'Тип посылки':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Документы")
        btn2 = types.KeyboardButton("Маленькие посылки")
        btn3 = types.KeyboardButton("Посылки среднего размера")
        btn4 = types.KeyboardButton("Большие посылки")
        markup.add(btn1, btn2, btn3, btn4)
        msg = bot.send_message(message.chat.id,
                               text="Выберите максимальный размер посылки, который Вы бы могли перевезти".format(
                                   message.from_user),
                               reply_markup=markup)
        bot.register_next_step_handler(msg, type_send)
    bot.register_next_step_handler(msg, true_or_false)


def new_name(message):
    info['name'] = message.text


def from_city(message):
    info['city1'] = message.text


def to_city(message):
    info['city2'] = message.text


def type_send(message):
    if message.text == "Документы":
        info['size'] = 0
    elif message.text == "Маленькие посылки":
        info['size'] = 1
    elif message.text == "Посылки среднего размера":
        info['size'] = 2
    elif message.text == "Большие посылки":
        info['size'] = 3


# connection.close()
bot.infinity_polling()

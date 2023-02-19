import pymysql
import telebot
from telebot import types
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

connection = pymysql.connect(host="localhost", port=3306, user="root", passwd="root", database="bot")
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")

# sql = """INSERT INTO offers(NAME, CITY, DATEOF, TELEGRAM_ID)
#    VALUES ('Aliaksei', 'Братислава', "10 мая", "@HEDGEH0G_1")"""
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


def search(date):
    sql = f"INSERT INTO package(NAME, CITY, TYPEOFPACK, DAY, TELEGRAM_ID) VALUES ('{info['name']}', '{info['city']}', '{info[date]}', '{info['telegramid']}"

    print(sql)
    # try:
    #     cursor.execute(sql)
    #     connection.commit()
    # except:
    #     connection.rollback()


def add(date):
    sql = f"INSERT INTO package(NAME, CITY, TYPEOFPACK, DAY, TELEGRAM_ID) VALUES ('{info['name']}', '{info['city']}', '{info[date]}', '{info['telegram.id}']}"

    try:
        cursor.execute(sql)
        connection.commit()
    except:
        connection.rollback()


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
        bot.send_message(message.chat.id, f"Выберете год поиска", reply_markup=calendar)
    elif message.text == "Перевозчик":
        flag = -1
        calendar, step = DetailedTelegramCalendar().build()
        bot.send_message(message.chat.id, f"Выберете год ваше поездки", reply_markup=calendar)
    elif message.text == "Беларусь":
        st = "Выберите город "
        if now == 1:
            info['country1'] = "Беларусь"
            st += "отправления"
        else:
            info['country2'] = "Беларусь"
            st += "назначения"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Минск")
        btn2 = types.KeyboardButton("Гомель")
        btn3 = types.KeyboardButton("Гродно")
        btn4 = types.KeyboardButton("Витебск")
        btn5 = types.KeyboardButton("Гомель")
        btn6 = types.KeyboardButton("Брест")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        bot.send_message(message.chat.id, text=st.format(message.from_user),
                         reply_markup=markup)

    elif message.text == "Словакия":
        st = "Выберите город "
        if now == 1:
            info['country1'] = "Словакия"
            st += "отправления"
        else:
            info['country2'] = 'Словакия'
            st += 'назначения'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Братислава")
        btn2 = types.KeyboardButton("Нитра")
        btn3 = types.KeyboardButton("Кошице")
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id,
                         text=st.format(message.from_user),
                         reply_markup=markup)
    elif message.text in ["Минск", "Гомель", "Гродно", "Витебск", "Гомель", "Брест"]:
        if now == 1:
            info['citifrom1'] = message.text
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn2 = types.KeyboardButton("Словакия")
            markup.add(btn2)
            bot.send_message(message.chat.id,
                             text="Выберите страну назначения".format(message.from_user),
                             reply_markup=markup)
            now += 1
        else:
            info['citifrom2'] = message.text
            print(info)

    elif message.text in ["Братислава", "Нитра", "Кошице"]:
        if now == 1:
            info['citifrom1'] = message.text
        else:
            info['citifrom2'] = message.text
            print(info)
            bot.send_message(message.chat.id,
                             text=f"Ваши данные были обработаны. Проверьте их правильность: Ваше имя: {info['name']}\nВаш телеграмм: @{info['telegramid']}\nГород отправления: {info['citifrom1']}\nГород прибытия: {info['citifrom2']}\nДень отправления: {info['date']}")
    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    result, key, step = DetailedTelegramCalendar().process(c.data)
    global flag
    if flag == 1:
        if not result and key:
            bot.edit_message_text(f"Выберите время Вашей поездки", c.message.chat.id, c.message.message_id,
                                  reply_markup=key)
        elif result:
            search(result)
            bot.edit_message_text(f"You selected {result}", c.message.chat.id, c.message.message_id)
    else:
        if not result and key:
            bot.edit_message_text(f"Выберите начиная с какой даты вам бы хотелось отследить перевозчиков",
                                  c.message.chat.id, c.message.message_id, reply_markup=key)
        elif result:
            info['date'] = result
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Беларусь")
            btn2 = types.KeyboardButton("Словакия")
            markup.add(btn1, btn2)
            bot.send_message(c.message.chat.id,
                             text="Выберите страну отправления".format(c.from_user),
                             reply_markup=markup)


connection.close()
bot.infinity_polling()

import telebot, psycopg2
from telebot import types

bot = telebot.TeleBot('7056258134:AAF1DhOPSw5Q9OT8jruWUbZ_xC5nSl3ia-U')

def genreslist():
    try:
        connection = psycopg2.connect(
            host = "127.0.0.1",
            user = "postgres",
            password = "postgres",
            database = "postgres")
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute('''SELECT * FROM genres''')
            connection.commit()
            genres=cursor.fetchall()
    except Exception as _ex:
        print ('Error:', _ex)
    finally:
        if connection:
            connection.close()
    return genres
def bookslist():
    try:
        connection = psycopg2.connect(
            host = "127.0.0.1",
            user = "postgres",
            password = "postgres",
            database = "postgres")
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute('''SELECT * FROM books''')
            connection.commit()
            books=cursor.fetchall()
    except Exception as _ex:
        print ('Error:', _ex)
    finally:
        if connection:
            connection.close()
    return books

genres = genreslist()

@bot.message_handler(commands=['start'])
def start (message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Добавить книгу', callback_data='adding'))
    bot.send_message(message.chat.id, 'Действие', reply_markup=markup)

@bot.callback_query_handler(func = lambda callback:True)
def buttoms (callback):
    if callback.data == 'adding':
        bot.send_message(callback.message.chat.id, 'Название книги')
        bot.register_next_step_handler(callback.message, adding_name)
    if callback.data == 'watch':
        books = bookslist()
        bookslistprint=str()
        for i in range(len(books)):
            bookslistprint=bookslistprint + books[i][1] + '\n' + books[i][2] + '\n\n'
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Посмотреть весь список', callback_data='watch'))
        markup.add(types.InlineKeyboardButton('Перейти на сайт', url='https://pashaiden.tilda.ws/biblioteka'))
        bot.send_message(callback.message.chat.id, 'Список: \n\n' + bookslistprint, reply_markup=markup)
    for i in range(len(genres)):
        if callback.data == genres[i][2]:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Посмотреть весь список', callback_data='watch'))
            markup.add(types.InlineKeyboardButton('Перейти на сайт', url='https://pashaiden.tilda.ws/biblioteka'))
            bot.send_message(callback.message.chat.id, 'Книга добавлена', reply_markup=markup)


def adding_name (message):
    bot.send_message(message.chat.id, 'Автор')
    bot.register_next_step_handler(message, genre_name)

def genre_name (message):
    markup = types.InlineKeyboardMarkup()
    for i in range(len(genres)):
        markup.add(types.InlineKeyboardButton(genres[i][1], callback_data=genres[i][2]))
    bot.send_message(message.chat.id, 'Жанр:', reply_markup=markup)

bot.infinity_polling()
import telebot, psycopg2
from telebot import types

bot = telebot.TeleBot('7056258134:AAF1DhOPSw5Q9OT8jruWUbZ_xC5nSl3ia-U')


def dbaction(selection, query):
    try:
        connection = psycopg2.connect(
            host="127.0.0.1",
            user="postgres",
            password="postgres",
            database="postgres")
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(query) # <--- сюда передается SQL запрос
            connection.commit()
            if selection==1:
                datas=cursor.fetchall()
    except Exception as _ex:
        print ('Error:', _ex)
    finally:
        if connection:
            connection.close()
            if selection==1:
                return datas
def genreslist():
    genres=dbaction(1, '''SELECT * FROM genres''')
    return genres
def bookslist():
    books=(1, '''SELECT * FROM books''')
    return books


genres = genreslist()
bookforadd=[0, 0, 0, 0]

@bot.message_handler(commands=['start'])
def start (message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Добавить книгу', callback_data='adding'))
    bot.send_message(message.chat.id, 'Действие', reply_markup=markup)

@bot.callback_query_handler(func = lambda callback:True)
def buttoms (callback):

    # Добавление книги 1: запрос указания названия книги
    if callback.data == 'adding':
        bot.send_message(callback.message.chat.id, 'Название книги')
        bot.register_next_step_handler(callback.message, adding_name)

    # Просмотр списка книг
    if callback.data == 'watch':
        books = bookslist()
        bookslistprint=str()
        for i in range(len(books)):
            bookslistprint=bookslistprint + books[i][1] + '\n' + books[i][2] + '\n\n'
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Посмотреть весь список', callback_data='watch'))
        markup.add(types.InlineKeyboardButton('Перейти на сайт', url='https://pashaiden.tilda.ws/biblioteka'))
        bot.send_message(callback.message.chat.id, 'Список: \n\n' + bookslistprint, reply_markup=markup)

    # Добавление книги 4: добавление жанра, отчет о завершении добавления. Выбор дальнейшего действия.
    for i in range(len(genres)):
        if callback.data == genres[i][2]:
            bookforadd[3] = genres[i][1]

            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Посмотреть весь список', callback_data='watch'))
            markup.add(types.InlineKeyboardButton('Перейти на сайт', url='https://pashaiden.tilda.ws/biblioteka'))
            bot.send_message(callback.message.chat.id, 'Книга добавлена: \n\n' + bookforadd[1] + '\n' + bookforadd[2] + '\n' + bookforadd[3] + '\n' + str(bookforadd[0]), reply_markup=markup)

# Добавление книги 2: добавление названия книги, запрос указания автора
def adding_name (message):
    bookforadd[1]=message.text
    bot.send_message(message.chat.id, 'Автор')
    bot.register_next_step_handler(message, genre_name)

# Добавление книги 3: добавление автора, запрос выбора жанра
def genre_name (message):
    bookforadd[2]=message.text
    markup = types.InlineKeyboardMarkup()
    for i in range(len(genres)):
        markup.add(types.InlineKeyboardButton(genres[i][1], callback_data=genres[i][2]))
    bot.send_message(message.chat.id, 'Жанр:', reply_markup=markup)

bot.infinity_polling()
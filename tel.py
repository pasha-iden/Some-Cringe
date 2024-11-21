import telebot, psycopg2
from telebot import types

bot = telebot.TeleBot('7056258134:AAF1DhOPSw5Q9OT8jruWUbZ_xC5nSl3ia-U')


def dbaction(selection, query):
    datas=None
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
    return datas
def genreslist():
    genres=dbaction(1, '''SELECT * FROM genres''')
    return genres
def bookslist():
    books=''
    gl=genreslist()
    for i in range(len(gl)):
        gbl=chgenrelist(gl[i][1])
        if gbl>[]:
            books=books + gl[i][1] + ': \n\n'
            for l in range(len(gbl)):
                books=books + gbl[l][1] + '\n' + gbl[l][2] + '\n\n'
    # books=dbaction(1, '''SELECT * FROM books''')
    return books
def chgenrelist(choisengenre):
    query="SELECT * FROM books WHERE genre='" + choisengenre + "' ORDER BY numingenre"
    cgl=dbaction(1, query)
    return cgl

def bookadding (infoaboutbook):
    i = dbaction(1, '''SELECT MAX(id) FROM books''')
    infoaboutbook[0]=i[0][0]+1
    query='''INSERT INTO books VALUES (''' + str(infoaboutbook[0]) + ", '" + infoaboutbook[1] + "', '" + infoaboutbook[2] + "', '" + infoaboutbook[3] + "', '" + str(infoaboutbook[4]) + "')"
    n=dbaction(0, query)
def bookaddinginto (infoaboutbook):

    # определение списка книга, которые нужно сдвинуть в списке жанра
    query = "SELECT id, numingenre FROM books WHERE genre='" + infoaboutbook[3] + "' AND numingenre>" + str(int(infoaboutbook[4])-1)
    renuberingbooks = dbaction(1, query)

    # сдвиг книг в жанре
    for i in range(len(renuberingbooks)):
        query = "UPDATE books SET numingenre =" + str(renuberingbooks[i][1]+1) + " WHERE id=" + str(renuberingbooks[i][0])
        n = dbaction(0, query)

    # добавление книги в список
    i = dbaction(1, '''SELECT MAX(id) FROM books''')
    query = '''INSERT INTO books VALUES (''' + str(i[0][0]+1) + ", '" + infoaboutbook[1] + "', '" + infoaboutbook[2] + "', '" + infoaboutbook[3] + "', '" + str(infoaboutbook[4]) + "')"
    n = dbaction(0, query)




genres = genreslist()
bookforadd=[0, 0, 0, 0, 0]

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
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Посмотреть весь список', callback_data='watch'))
        markup.add(types.InlineKeyboardButton('Перейти на сайт', url='https://pashaiden.tilda.ws/biblioteka'))
        bot.send_message(callback.message.chat.id, 'Список: \n\n' + books, reply_markup=markup)

    # Добавление книги 4: добавление жанра, запрос указания места в списке книг жанра.
    for i in range(len(genres)):
        if callback.data == genres[i][2]:
            bookforadd[3] = genres[i][1]
            choisengenrebooks=chgenrelist(bookforadd[3])
            if choisengenrebooks==[]:
                bookforadd[4]=1
                bookadding(bookforadd)
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton('Посмотреть весь список', callback_data='watch'))
                markup.add(types.InlineKeyboardButton('Перейти на сайт', url='https://pashaiden.tilda.ws/biblioteka'))
                bot.send_message(callback.message.chat.id, 'Книга добавлена: \n\n Книга: ' + bookforadd[1] + '\n Автор: ' + bookforadd[2] + '\n Жанр: ' + bookforadd[3] + '\n Место в списке: ' + str(bookforadd[4]), reply_markup=markup)
            else:
                bl=str()
                for l in range(len(choisengenrebooks)):
                    bl=bl + str(choisengenrebooks[l][4]) + '. ' + choisengenrebooks[l][1] + '\n' + choisengenrebooks[l][2] + '\n\n'
                bot.send_message(callback.message.chat.id, 'На какое место поставить эту книгу: \n\n' + str(bl))
                bot.register_next_step_handler(callback.message, accepting)

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
        if genres [i][2]=='russian':
            markup.add(types.InlineKeyboardButton('Русская художественная литература', callback_data=genres[i][2]))
        elif genres [i][2]=='foreign':
            markup.add(types.InlineKeyboardButton('Зарубужная художественная литература', callback_data=genres[i][2]))
        else:
            markup.add(types.InlineKeyboardButton(genres[i][1], callback_data=genres[i][2]))
    bot.send_message(message.chat.id, 'Жанр:', reply_markup=markup)

# Добавление книги 5: добавление места книги в списке книг жанра, отчет о завершении добавления. Выбор дальнейшего действия.
def accepting (message):
    bookforadd[4] = message.text
    if int(bookforadd[4]) > len(chgenrelist(bookforadd[3])):
        bookadding(bookforadd)
    else:
        bookaddinginto(bookforadd)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Посмотреть весь список', callback_data='watch'))
    markup.add(types.InlineKeyboardButton('Перейти на сайт', url='https://pashaiden.tilda.ws/biblioteka'))
    bot.send_message(message.chat.id, 'Книга добавлена: \n\n Книга: ' + bookforadd[1] + '\n Автор: ' + bookforadd[2] + '\n Жанр: ' + bookforadd[3] + '\n Место в списке: ' + str(bookforadd[4]), reply_markup=markup)

bot.infinity_polling()
import telebot
from telebot import types

bot = telebot.TeleBot('7056258134:AAF1DhOPSw5Q9OT8jruWUbZ_xC5nSl3ia-U')

@bot.message_handler(commands=['start'])
def start (message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Добавить книгу', callback_data='adding'))
    bot.send_message(message.chat.id, 'Действие', reply_markup=markup)

@bot.callback_query_handler(func = lambda callback:True)
def adding (callback):
    if callback.data == 'adding':
        bot.send_message(callback.message.chat.id, 'Название книги')
        bot.register_next_step_handler(callback.message, adding_name)

def adding_name (message):
    bot.send_message(message.chat.id, 'Автор')
    bot.register_next_step_handler(message, accepting)

def accepting (message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Перейти на сайт', url='https://pashaiden.tilda.ws/biblioteka'))
    bot.send_message(message.chat.id, 'Книга добавлена', reply_markup=markup)

bot.infinity_polling()
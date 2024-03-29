
import datetime

import calendar
from xml.dom.xmlbuilder import _name_xform

from telegramcalendar import create_calendar
import telebot
from telebot import types
from ORMClass_STBot import *



TOKEN = '870672383:AAE9d8p3SRMrMV3L15RwRzYZwVDThCLPS4g'
bot = telebot.TeleBot(TOKEN)

def message_add(new_message):
    # add message
    create_message = Message()
    create_message.message_id = new_message.message_id
    create_message.date = datetime.datetime.fromtimestamp(new_message.date)
    create_message.text = new_message.text
    create_message.add()

    # add FromSomeone
    create_someone = FromSomeone()
    create_someone.message_id = new_message.message_id
    create_someone.someone_id = new_message.from_user.id
    create_someone.is_bot = new_message.from_user.is_bot
    create_someone.first_name = new_message.from_user.first_name
    create_someone.last_name = new_message.from_user.last_name
    create_someone.username = new_message.from_user.username
    create_someone.language_code = new_message.from_user.language_code
    create_someone.add()

    # add Entities
    # create_entities = Entities()
    # create_entities.message_id = new_message.message_id
    # create_entities.length = new_message.entities.length
    # create_entities.offset = new_message.entities.offset
    # create_entities.type = new_message.entities.type
    # create_entities.add()



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Hi, {message.chat.first_name}")
    message_add(message)

    # print(message)
    # n_book = Book()
    # n_book.title = 'book5'
    # n_book.add()

    # n_book.author = 'andrii'
    # n_book.pages = 27
    # n_book.published = datetime.datetime.now()
    # n_book.id = 1





@bot.message_handler(commands = ['url'])
def url(message):
    markup = types.InlineKeyboardMarkup()
    btn_my_site= types.InlineKeyboardButton(text='Наш сайт', url='https://habrahabr.ru')
    markup.add(btn_my_site)
    bot.send_message(message.chat.id, "Нажми на кнопку и перейди на наш сайт.", reply_markup = markup)

@bot.message_handler(commands = ['switch'])
def switch(message):
    markup = types.InlineKeyboardMarkup()
    switch_button = types.InlineKeyboardButton(text='Try', switch_inline_query="Telegram")
    markup.add(switch_button)
    bot.send_message(message.chat.id, "Выбрать чат", reply_markup = markup)
    print(markup)

@bot.message_handler(commands=['calendar'])
def get_calendar(message):
    now = datetime.datetime.now() #Текущая дата
    chat_id = message.chat.id
    date = (now.year, now.month)
    #current_shown_dates = {}
    #current_shown_dates[chat_id] = date #Сохраним текущую дату в словарь
    markup = types.InlineKeyboardMarkup()
    row_set = create_calendar(now.year,now.month)

    for i in row_set:
        markup.row(*i)
    bot.send_message(message.chat.id, "Пожалйста, выберите дату", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, "Спробуй команди /start /help /url /switch /calendar")
	print(message)


# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
# 	bot.reply_to(message, message.text)
#
# @bot.message_handler(content_types=['text'])
# def send_welcome(message):
# 	bot.reply_to(message, "Really?")

bot.polling()


import telebot
from random import randint
import SQLConntection
import sqlite3
import config
from decorators import checking_status


TOKEN = config.API_KEY
bot = telebot.TeleBot(TOKEN)

database = config.PATH_TO_DATABASE
dbGet = SQLConntection.DatabaseGet(database)
dbPost = SQLConntection.DatabasePost(database)

queueDist = {}  # Количество заданий у пользователя


def add_or_edit_to_queue(ID, number):
    queueDist[ID] = number


def del_from_queue(ID):
    del queueDist[ID]


def get_ru_word_to_adding(message):
    sent = bot.send_message(message.chat.id, "Введите перевод этого слова.")
    bot.register_next_step_handler(sent, add_new_word, str(message.text).lower())


def add_new_word(message, enWord):
    ruWord = str(message.text).lower()
    try:
        dbPost.add_word(enWord, ruWord, 1)
        bot.send_message(message.chat.id, ("Слово " + enWord + " добавленно в базу"))
    except sqlite3.IntegrityError:
        bot.send_message(message.chat.id, ("Слово " + enWord + " уже есть в базе"))


def inline_create_kb_with_words(messageID):
    limit = 4
    randomN = randint(0, limit-1)

    enList, ruList = dbGet.get_word_of_limit(limit)

    buttonList = []
    for i in range(limit):
        if i == randomN:
            button_y = telebot.types.InlineKeyboardButton(ruList[i], callback_data='true_word')
            buttonList.append(button_y)
        else:
            button_n = telebot.types.InlineKeyboardButton(ruList[i], callback_data='false_word')
            buttonList.append(button_n)

    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2).add(*buttonList)
    text = "Как переводиться слово " + enList[randomN] + "?"

    bot.send_message(messageID, text, reply_markup=keyboard)


@bot.message_handler(commands=['start'])
def start(message):

    username = str(message.from_user.first_name) + " " \
               + str(message.from_user.last_name) + " " \
               + str(message.from_user.username)
    chatId = message.from_user.id
    level = str(1)
    print(message.from_user.id, "\n",
          message.from_user.first_name, "\n",
          message.from_user.last_name, "\n",
          message.from_user.username, "\n",
          username)
    try:
        dbPost.init_user(chatId, username, level)
        bot.send_message(message.chat.id, "Привет. Это бот для изучения новых английских слов.")
    except Exception:
        bot.send_message(message.chat.id, "Привет. Кажется ты уже зарегистрирован в нашей базе.")


@bot.message_handler(commands=['help'])
def help_command(message):
    text = 'Команды get и getquestion можно расширить одним аргументом в формте "/команда [аргумент]". ' \
           'Этот аргумент задает количество слов выдаваемых на один ввод команды.'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['get'])
def get(message):
    try:
        status = message.text.split()[1:][0]
    except IndexError:
        status = 1
    try:
        status = int(status)
    except Exception:
        status = 1
        bot.send_message(message.chat.id, "Кажется вы ввели не число. Я ввел вместо вас 1.")

    if status > 50:
        bot.send_message(message.chat.id, "Вы превысили максимальный заприс - 50. Я ввел вместо вас 1.")
        status = 1
    try:
        res = ''
        enList, ruList = dbGet.get_word_of_limit(status)
        for i in range(len(enList)):
            res += enList[i] + ' - ' + ruList[i] + "\n"
        bot.send_message(message.chat.id, res)
    except Exception:
        bot.send_message(message.chat.id, "Возникла непредвиденная ошибка.")


@bot.message_handler(commands=['getquestion'])
def getquestion(message):
    try:
        status = message.text.split()[1:][0]
    except IndexError:
        status = 5
    try:
        status = int(status)
    except Exception:
        status = 5
        bot.send_message(message.chat.id, "Кажется вы ввели не число. Я ввел вместо вас 5.")

    if status > 50:
        bot.send_message(message.chat.id, "Вы превысили максимальный заприс - 50. Я ввел вместо вас 1.")
        status = 5
    try:
        bot.send_message(message.from_user.id, "Подождите, генерирую ваши задания.")
        if status == 1:
            inline_create_kb_with_words(message.from_user.id)
        else:
            add_or_edit_to_queue(message.from_user.id, status - 1)
            inline_create_kb_with_words(message.from_user.id)
    except Exception:
        bot.send_message(message.chat.id, "Возникла непредвиденная ошибка.")


@bot.message_handler(commands=['addword'])
@checking_status
def start(message):
    sent = bot.send_message(message.chat.id, "Введите новое слово на английском.")
    bot.register_next_step_handler(sent, get_ru_word_to_adding)


@bot.callback_query_handler(lambda c: c.data and c.data.startswith('true_word'))
def process_callback_kb1(callback_query):
    bot.send_message(callback_query.from_user.id, "Да")
    ID = callback_query.from_user.id
    if ID in queueDist:
        if queueDist[ID] == 1:
            del_from_queue(ID)
            inline_create_kb_with_words(ID)
        else:
            add_or_edit_to_queue(ID, queueDist[ID] - 1)
            inline_create_kb_with_words(ID)
    else:
        bot.send_message(ID, "Это все.")


@bot.callback_query_handler(lambda c: c.data and c.data.startswith('false_word'))
def process_callback_kb1(callback_query):
    bot.send_message(callback_query.from_user.id, "Нет")


bot.polling(none_stop=True)

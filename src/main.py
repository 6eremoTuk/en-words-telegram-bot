import telebot
from random import randint
import SQLConnection
import sqlite3
import config
from decorators import checking_status


print('Starting EngTeleBot v.0.2.0')
bot = telebot.TeleBot(config.API_KEY)
print('Bot started successfully')

print('---------------------')

print('Connecting to database')
dbGet = SQLConnection.DatabaseGet(config.PATH_TO_DATABASE)
dbPost = SQLConnection.DatabasePost(config.PATH_TO_DATABASE)
print('Database connecting successfully')

queueDist = {}  # Количество заданий у пользователя


def add_or_edit_to_queue(ID, number):
    """
    Эта функция добавляет пользователя с количеством заданий в словарь или изменяет количество заданий пользователя.

    :param ID: id пользователя
    :param number: количество заданий пользователя
    """
    queueDist[ID] = number


def del_from_queue(ID):
    """
        Эта функция удаляет пользователя по id из списка заданий.

        :param ID: id пользователя
        """
    del queueDist[ID]


def get_ru_word_to_adding(message):
    """Эта промежуточная функция запрашивает перевод слова и вызывает фугкцию add_new_word
     с параметром слова не английском, полученного из message и сообщением с русским словом."""
    sent = bot.send_message(message.chat.id, "Введите перевод этого слова.")
    bot.register_next_step_handler(sent, add_new_word, str(message.text).lower())


def add_new_word(message, enWord):
    """Эта функция вытаскивает из сообщения русское словоб и в качестве второго аргумента пулучает английское слово.
    Она добавляет слово и его перевод в базу и в случае успеха отправляет пользователь положительное сообщение,
    а в случае если это слово уже есть в базе отправляет отрицательное сообщение."""
    ruWord = str(message.text).lower()
    try:
        dbPost.add_word(enWord, ruWord, 1)
        bot.send_message(message.chat.id, ("Слово " + enWord + " добавленно в базу"))
    except sqlite3.IntegrityError:
        bot.send_message(message.chat.id, ("Слово " + enWord + " уже есть в базе"))


def inline_create_kb_with_words(messageID):
    """Эта функция спрашивае у пользователя перевод случайного слова и предлагает клавиатуру с четырьмя
    русскими словами одно из которых правильное. При нажатии на кнопку срабатывает один из двух callback-ов."""
    limit = 4  # количество слов
    randomN = randint(0, limit-1)  # случайным образом выбирает номер правильного слова

    enList, ruList = dbGet.get_word_of_limit(limit)  # получает limit слов с переводом из базы

    buttonList = []  # список кнопок
    for i in range(limit):  # повторяется limit раз
        if i == randomN:  # если слово правильное создает кнопку с текстом перевода слова и callback-ом true_word
            button_y = telebot.types.InlineKeyboardButton(ruList[i], callback_data='true_word')
            buttonList.append(button_y)
        else:  # иначесоздает кнопку с текстом перевода слова и callback-ом false_word
            button_n = telebot.types.InlineKeyboardButton(ruList[i], callback_data='false_word')
            buttonList.append(button_n)

    keyboard = telebot.types.InlineKeyboardMarkup(row_width=2).add(*buttonList)  # создает клавиатуру из кнопок
    text = "Как переводиться слово " + enList[randomN] + "?"

    bot.send_message(messageID, text, reply_markup=keyboard)


@bot.message_handler(commands=['start'])
def start(message):
    username = str(message.from_user.first_name) + " " \
               + str(message.from_user.last_name) + " " \
               + str(message.from_user.username)  # получает из сообщения имя пользователя
    chatId = message.from_user.id  # получает из сообщения id пользователя
    level = str(1)
    try:  # если пользователя нет в базе то добавляет его
        dbPost.init_user(chatId, username, level)
        bot.send_message(message.chat.id, "Привет. Это бот для изучения новых английских слов.")
    except Exception:  # иначе отправляет сообщение об ошибке
        bot.send_message(message.chat.id, "Привет. Кажется ты уже зарегистрирован в нашей базе.")


@bot.message_handler(commands=['help'])
def help_command(message):
    text = 'Команды get и get_question можно расширить одним аргументом в формте "/команда [аргумент]". ' \
           'Этот аргумент задает количество слов или вопросов, выдаваемых на один ввод команды.'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['get'])
def get(message):
    """Эта функция отправляет пользователю слова с перевозом из базы."""
    try:  # если аргумент есть и это число, то status = аргумент
        status = message.text.split()[1:][0]
        status = int(status)
        if status > 50:  # если аргумент больше 50, то status = 1
            bot.send_message(message.chat.id, "Вы превысили максимальный запрос - 50. Я ввел вместо вас 1.")
            status = 1
    except Exception:  # иначе при любой ошибке status = 1
        status = 1
        bot.send_message(message.chat.id, "Выдаю одно слово.")

    try:
        res = ''
        enList, ruList = dbGet.get_word_of_limit(status)  # получеет случайные слова, количество которых = status
        for i in range(len(enList)):  # берет по одному слову из списка и добавляет его к готовому тексту
            res += enList[i] + ' - ' + ruList[i] + "\n"
        bot.send_message(message.chat.id, res)
    except Exception:
        bot.send_message(message.chat.id, "Возникла непредвиденная ошибка.")


@bot.message_handler(commands=['get_question'])
def get_question(message):
    """Эта функция отправляет пользователю вопрос и возможно зпускает цепочку вопросов"""
    try:  # если аргумент есть и это число, то status = аргумент
        status = message.text.split()[1:][0]
        status = int(status)
        if status > 50:  # если аргумент больше 50, то status = 5
            bot.send_message(message.chat.id, "Вы превысили максимальный запрос - 50. Я ввел вместо вас 5.")
            status = 5
    except Exception:  # иначе при любой ошибке status = 5
        status = 5
        bot.send_message(message.chat.id, "Выдаю пять вопросов.")

    try:
        bot.send_message(message.from_user.id, "Подождите, генерирую ваши задания.")
        if status == 1:  # если вопрос 1 то отправляет вопрос пользователю
            inline_create_kb_with_words(message.from_user.id)
        else:  # иначе добавляет количество оставшихся вопросов в очередь и отправляет пользователю вопрос
            add_or_edit_to_queue(message.from_user.id, status - 1)
            inline_create_kb_with_words(message.from_user.id)
    except Exception:
        bot.send_message(message.chat.id, "Возникла непредвиденная ошибка.")


@bot.message_handler(commands=['add_word'])
@checking_status  # функция доступна только администраторам
def add_word(message):
    """Эта функция запускает цепочку добавления слова. Она запрашивает у пользователя слово на английском
    и вызывает функцию get_ru_word_to_adding"""
    sent = bot.send_message(message.chat.id, "Введите новое слово на английском.")
    bot.register_next_step_handler(sent, get_ru_word_to_adding)


@bot.callback_query_handler(lambda c: c.data and c.data.startswith('true_word'))
def true_word(callback_query):
    """Эта функция срабатывает, если пользователь выбрал правильное слово."""
    bot.send_message(callback_query.from_user.id, "Да")
    ID = callback_query.from_user.id
    if ID in queueDist:  # если у пользователя еще есть вопросы в очереди, то продолжает задавать их
        if queueDist[ID] == 1:  # если остался 1 вопрос то удаляет пользователя из очереди
            del_from_queue(ID)
            inline_create_kb_with_words(ID)
        else:  # иначе уменьшает количество его вопросов в очереди на 1
            add_or_edit_to_queue(ID, queueDist[ID] - 1)
            inline_create_kb_with_words(ID)
    else:
        bot.send_message(ID, "Это все.")


@bot.callback_query_handler(lambda c: c.data and c.data.startswith('false_word'))
def false_word(callback_query):
    """Эта функция срабатывает, если пользователь выбрал правильное слово."""
    bot.send_message(callback_query.from_user.id, "Нет")


bot.polling(none_stop=True)

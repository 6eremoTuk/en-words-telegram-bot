""" Бот для изучения англитйских слов.
 Вначале пользователю даеться входной тест для определения уровня словарного запаса (в дальнейшем можно перепройти).
 По итогам тестирования пользователь получит направление к определенной базе слов (их будет несколько), соответствующей
 его уровню. У пользователя будет графа с номерами неизученных слов. Постепенно по мере их изучения некоторые номера
 будут стираться. Пока планируется две функции: изучение новых слов (берет неизученные слова из соответствующей графы) и
 сразу тестирование на их знание и функция тестирования на знание всех изученных слов из базы. Она будет представлять
 собой вопрос 'Как переводиться *слово*?' и 4 варианта ответа один из которых правильный. Еще можно добавить лидерборд
 на количество изученных новых слов сегдня или на пройденные тести и средний результат по ним.
 В дальнейшем возможен переход на новый уровень словарного запаса, следовательгно переход на новую базу.
 Бот может собирать имя пользователя, его id, уровень словарного запаса, неизученные слова, средний результат по тестам
 (процент правильных ответов) и возможно что-то еще."""


# import databaseConnectingLibrary
# import telegramBotLibrary

DATABASE = "database.db"


class GetDatabase:
    """ Class for posting data to the database """
    def __init__(self, pathToDB):
        """ Connection to the database. Creating a cursor """
        pass

    def get_something(self, inputData):
        """ Makes a request to the database and returns the result """
        pass


class PostDatabase:
    """ Class for posting data to the database """
    def __init__(self, pathToDB):
        """ Connection to the database. Creating a cursor """
        pass

    def post_something(self, inputData):
        """ Posts data into a database and commits it """
        pass


class TelegramBot:
    """ Class for connecting to the teleBot and  manage it"""
    TOKEN = ""

    def __init__(self):
        """ Connecting to the teleBot """
        pass

    def start(self):
        """ Command for start. Posting user data to database """
        pass

    def any_command(self):
        """ Any command to manage bot """
        pass


class Main:
    """ Main class """
    def __init__(self):
        """ Initialization """
        self.getDatabase = GetDatabase(DATABASE)
        self.postDatabase = PostDatabase(DATABASE)
        self.teleBot = TelegramBot()

    def start(self):
        """ Start bot """
        self.teleBot.start()


main = Main()
main.start()

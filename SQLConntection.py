import sqlite3


class DatabaseGet:

    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def get_word_of_limit(self, limit):
        enList = []
        ruList = []
        _SQL = """SELECT * FROM words
                    ORDER BY RANDOM()
                    LIMIT (?)"""
        word = self.cursor.execute(_SQL, (limit, )).fetchall()
        for i in word:
            enList.append(i["enWord"])
            ruList.append(i["ruWord"])
        return enList, ruList

    def __del__(self):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()


class DatabasePost:

    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def init_user(self, user_chat_id, user_name, level):
        _SQL = """INSERT INTO users
                    (user_chat_id, user_name, level)
                    VALUES
                    (?, ?, ?)"""
        self.cursor.execute(_SQL, (user_chat_id, user_name, level))
        self.connection.commit()

    def add_word(self, en_word, ru_word, level):
        _SQL = """INSERT INTO words
                    (enWord, ruWord, level)
                    VALUES
                    (?, ?, ?)"""
        self.cursor.execute(_SQL, (en_word, ru_word, level))
        self.connection.commit()

    def __del__(self):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

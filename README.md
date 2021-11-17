# English Telegram Bot

Телеграм бот для помощи в изучении английских слов.

Написан с использованием Python 3.8.
Для хранения данных используется база данных SQLite (`database.db`).

## Зависимости

Зависимости указаны в `requirements.txt`. Установка зависимостей осуществляется через 

```shell
pip3 install -r requirements.txt
```

## Настройка и запуск

Настройка осуществляется при помощи заполнения файла `config.py`.

Используемые параметры:

- `API_KEY` - Token бота в Telegram. Методика получения ключа описана [в документации](https://core.telegram.org/bots#6-botfather)
- `PATH_TO_DATABASE` - путь к базе данных SQLite

Запуск осуществляется:

```shell
python3 main.py
```

Если запуск прошел успешно, то в консоли Вы увидите сообщение о том, что сервис запущен и готов к работе.

```shell
Starting EngTeleBot v.0.2.0
Bot started successfully
-----------------------
Connecting to database
Database connecting successfully
```

## Лицензия

Распространяется "как есть" т.е. даром :)

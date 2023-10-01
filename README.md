# green-tech-bot

A telegram bot for Green.tech, the environmental club of MIPT.

## How to run the bot locally (Fedora Linux)

First, create and activate a python virtual environment. Using it allows you to
avoid installing Python packages globally which could break system tools or
other projects
```
python3 -m venv .venv
source .venv/bin/activate
```

If necessary, upgrade `pip` in your virtual environment.
```
pip install --upgrade pip
```

Install required python packages
```
pip install -r requirements.txt
```

Make sure to have `bot_secrets.py` filled and run the code
```
python green-tech-bot/main.py
```

Press Ctrl-C on the command line or send a signal to the process to stop the
bot. To deactivate your virtual environment, simply run
```
deactivate
```

## Текущие задачи разработки

1) Создать БД MySQL/PostgreSQL

Старая структура БД:
```
users: id first_name last_name username state subscription cnt authorized [last_usage] <temporary info>

traffic: date actions_count users_count
journal: datetime type where what chat_id

subscriptions: id where what
locations: name latitude longitude visible(bool)
fractions: name
stations: location_id, fraction_id, visible
map_locations: name latitude longitude visible
map_fractions: name visible core(=important, bool)
map_stations: location_id, fraction_id, text
```

Новая структура БД: [new-db-project/db_description.md](new-db-project/db_description.md)

2) Подготовить скрипты для переноса БД
3) Сделать код рабочим + добавить логирование
4) Подключить карту к той же б/д
5) Удобное тестирование, релиз

6) Перевести на новую версию `python-telegram-bot`.
В ней каноничный способ запуска бота такой:

```python
if __name__ == "__main__":
    application = ApplicationBuilder().token('TOKEN').build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    # other handlers...

    application.run_polling()
```

7) Сделать код красивым
8) ???
9) Добавить проверку, что кто-то подписан на точку, о которой зарепорчено
10) Жёстко всё прокомментировать

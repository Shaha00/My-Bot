import random
import sqlite3
from config import bot


def sql_create():
    global db, cursor
    db = sqlite3.connect("bot.sqlite3")
    cursor = db.cursor()

    if db:
        print('База данных подключена!')

    db.execute("CREATE TABLE IF NOT EXISTS anketa "
               "(id INTEGER PRIMARY KEY, username TEXT, "
               "name TEXT, id2 INTEGER, direction TEXT, "
               "age INTEGER, groupp TEXT)")
    db.commit()


async def sql_command_insert(state):
    async with state.proxy() as data:
        cursor.execute("INSERT INTO anketa VALUES "
                       "(?, ?, ?, ?, ?, ?, ?)", tuple(data.values()))
        db.commit()


async def sql_command_random(message):
    result = cursor.execute("SELECT * FROM anketa").fetchall()
    random_user = random.choice(result)
    await message.answer(f'Group - {random_user[6]}'
                         f'\nName - {random_user[2]}'
                         f'\nMentor_id - {random_user[3]}'
                         f'\nDirection - {random_user[4]}'
                         f'\nAge - {random_user[5]}'
                         f'\n{random_user[1]}')


async def sql_command_all():
    return cursor.execute("SELECT * FROM anketa").fetchall()


async def sql_command_delete(user_id):
    cursor.execute("DELETE FROM anketa WHERE id = ?", (user_id,))
    db.commit()


async def sql_command_get_all_ids():
    return cursor.execute("SELECT id FROM anketa").fetchall()

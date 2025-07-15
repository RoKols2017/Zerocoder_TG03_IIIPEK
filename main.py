import asyncio
import os
import random
import sqlite3
import tempfile


from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv


def slq_execute(db_path = 'school_data.db',query = None):
    if query:
        try:
            db = sqlite3.connect(db_path)
            cursor = db.cursor()
            cursor.execute(query)
            db.commit()
            db.close()
            return True
        except:
            return False
    else:
        return False

def sql_create(db_path = 'school_data.db'):
    query = """
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        grade INTEGER)
    """
    return slq_execute(db_path,query)




load_dotenv()
TOKEN = os.getenv('TOKEN')
if sql_create():
    print('База данных создана')
else:
    print('Какая-то ошибка при работе с БД')

bot = Bot(token=TOKEN)
dp = Dispatcher()


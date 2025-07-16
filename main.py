import asyncio
import os
import random
import tempfile


from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from dbwork import *
from utils import set_loglevel

class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()


load_dotenv()
TOKEN = os.getenv('TOKEN')
set_loglevel(level=os.getenv('LOG_LEVEL', 'INFO'))

db_path = os.getenv('DB_PATH')
if db_create(db_path):
    print('База данных успешно создана или уже существует')
else:
    print('Какая-то ошибка при работе с БД')

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('Как зовут ученика?')
    await state.set_state(Form.name)

@dp.message(Command('list'))
async def cmd_list(message: Message):
    students = db_select(db_path,'students')
    if len(students) == 0: return await message.answer('Список учеников пуст') # if empty list
    for student in students:
        await message.answer(f'{student[1]} {student[2]} лет в {student[3]} классе')

@dp.message(Command('class'))
async def cmd_class(message: Message, command: CommandObject):
    class_number = command.args
    students = db_select(db_path,'students', {'grade': class_number})
    if len(students) == 0: return await message.answer(f'Список учеников класса {class_number} пуст') # if empty list
    for student in students:
        await message.answer(f'{student[1]} {student[2]} лет в {student[3]} классе')

@dp.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('''Я умею выполнять такие команды:
    /start - Запустить бота
    /help - Помощь
    /list - Список учеников в классах
    /class <класс> - Список учеников в классе
    ''')

@dp.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Сколько лет ученику?')
    await state.set_state(Form.age)

@dp.message(Form.age)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('В каком классе ученик учится?')
    await state.set_state(Form.grade)

@dp.message(Form.grade)
async def process_grade(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)
    data = await state.get_data()
    if db_add(db_path,'students', data):
        await message.answer(f'Добавлен ученик {data["name"]} {data["age"]} лет в {data["grade"]} классе')
    else:
        await message.answer('Какая-то ошибка при работе с БД, проверьте данные (возраст от 1 до 150, класс от 1 до 12)')
    await state.finish()


if __name__ == '__main__':
    dp.run_polling(bot)








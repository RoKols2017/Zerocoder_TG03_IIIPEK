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


# Обработка команды /start: начало диалога, запрос имени ученика
@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('Как зовут ученика?')
    await state.set_state(Form.name)

# Обработка команды /list: выводит список всех учеников
@dp.message(Command('list'))
async def cmd_list(message: Message):
    students = db_select(db_path,'students')
    if len(students) == 0: return await message.answer('Список учеников пуст') # if empty list
    for student in students:
        await message.answer(f'{student[1]} {student[2]} лет в {student[3]} классе')

# Обработка команды /class <номер>: выводит список учеников выбранного класса
@dp.message(Command('class'))
async def cmd_class(message: Message, command: CommandObject):
    class_number = command.args
    students = db_select(db_path,'students', {'grade': class_number})
    if len(students) == 0: return await message.answer(f'Список учеников класса {class_number} пуст') # if empty list
    for student in students:
        await message.answer(f'{student[1]} {student[2]} лет в {student[3]} классе')

# Обработка команды /help: выводит справку по командам
@dp.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('''Я умею выполнять такие команды:
    /start - Запустить бота
    /help - Помощь
    /list - Список учеников в классах
    /class <класс> - Список учеников в классе
    ''')

# Шаг FSM: обработка имени ученика, запрос возраста
@dp.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Сколько лет ученику?')
    await state.set_state(Form.age)

# Шаг FSM: обработка возраста, валидация, запрос класса
@dp.message(Form.age)
async def process_age(message: Message, state: FSMContext):
    # Валидация возраста
    try:
        age = int(message.text)
        if not (1 <= age <= 149):
            await message.answer('Возраст должен быть числом от 1 до 149. Пожалуйста, введите корректный возраст:')
            return
    except ValueError:
        await message.answer('Пожалуйста, введите возраст числом (от 1 до 149):')
        return
    await state.update_data(age=age)
    await message.answer('В каком классе ученик учится? (например: 1А, 5Б, 11)')
    await state.set_state(Form.grade)

# Шаг FSM: обработка класса, валидация, сохранение в БД
@dp.message(Form.grade)
async def process_grade(message: Message, state: FSMContext):
    # Валидация класса (разрешаем любые не слишком длинные строки, например: 1А, 5Б, 11)
    grade = message.text.strip()
    if not (1 <= len(grade) <= 5):
        await message.answer('Класс должен быть строкой длиной от 1 до 5 символов (например: 1А, 5Б, 11). Пожалуйста, введите корректный класс:')
        return
    await state.update_data(grade=grade)
    data = await state.get_data()
    # Дополнительная проверка возраста перед сохранением
    try:
        age = int(data.get('age', 0))
        if not (1 <= age <= 149):
            await message.answer('Возраст должен быть числом от 1 до 149. Пожалуйста, введите возраст заново:')
            await state.set_state(Form.age)
            return
    except Exception:
        await message.answer('Ошибка с возрастом. Пожалуйста, введите возраст заново:')
        await state.set_state(Form.age)
        return
    # Сохраняем данные в БД
    if db_add(db_path,'students', data):
        await message.answer(f'Добавлен ученик {data["name"]} {data["age"]} лет в {data["grade"]} классе')
    else:
        await message.answer('Ошибка при работе с БД. Проверьте данные и попробуйте снова.')
    await state.clear()


if __name__ == '__main__':
    dp.run_polling(bot)








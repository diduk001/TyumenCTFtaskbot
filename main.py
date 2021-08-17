from resources import Resources
from config import Config
from sqlalchemy import create_engine
import re
from aiogram import Bot, Dispatcher, executor, types
from models import User

bot = Bot(Config.BOT_TOKEN)
dp = Dispatcher(bot)

stage = 0
# Эти переменный в субд кинуть
user_name = ''
user_surname = ''
mail = ''
mail_valid = False
nickname = ''
city = ''
age = ''
grade = ''
school = ''
registration_complete = ''


@dp.message_handler(commands='start')  # Старт регистрации
async def start_cmd_handler(message: types.Message):
    global stage
    await message.answer(Resources.START_MSG)
    await message.answer(Resources.NAME)
    stage += 1


@dp.message_handler()  # Регистрация имени
async def name_handler(message: types.Message):
    global stage
    global user_name
    if stage == 1:
        user_name = message.text
    await message.answer(Resources.SURNAME)
    stage += 1


@dp.message_handler()  # Регистрация фамилии
async def surname_handler(message: types.Message):
    global stage
    global user_surname
    if stage == 2:
        user_surname = message.text
    await message.answer(Resources.MAIL)
    stage += 1


@dp.message_handler()  # Регистрация мыла
async def mail_handler(message: types.Message):
    global stage
    global mail
    if stage == 3:
        mail = message.text
    await message.answer(Resources.NICKNAME)
    stage += 1


@dp.message_handler()  # Регистрация ника
async def nickname_handler(message: types.Message):
    global stage
    global nickname
    if stage == 4:
        nickname = message.text
    await message.answer(Resources.CITY)
    stage += 1


@dp.message_handler()  # Регистрация города
async def city_handler(message: types.Message):
    global stage
    global city
    if stage == 5:
        city = message.text
    await message.answer(Resources.AGE)
    stage += 1


@dp.message_handler()  # Регистрация возраста
async def age_handler(message: types.Message):
    global stage
    global age
    if stage == 6:
        age = message.text
    await message.answer(Resources.GRADE)
    stage += 1


@dp.message_handler()  # Регистрация класса
async def grade_handler(message: types.Message):
    global stage
    global grade
    if stage == 7:
        grade = message.text
    await message.answer(Resources.SCHOOL)
    stage += 1


@dp.message_handler()  # Регистрация школы
async def school_handler(message: types.Message):
    global stage
    global school
    if stage == 7:
        school = message.text
    await message.answer(Resources.REGISTRATION_COMPLETE)
    school += 1


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

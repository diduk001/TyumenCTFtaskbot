from resources import Resources
from config import Config
import re
from aiogram import Bot, Dispatcher, executor, types

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


@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message):
    global stage
    await message.answer(Resources.START_MSG)
    await message.answer(Resources.NAME)
    stage += 1


@dp.message_handler()
async def name_handler(message: types.Message):
    global stage, user_name, user_surname, mail, mail_valid, nickname, city, age, grade, school, registration_complete
    if stage == 1:
        user_name = message.text
        await message.answer(Resources.SURNAME)
        stage += 1
    elif stage == 2:
        user_surname = message.text
        await message.answer(Resources.MAIL)
        stage += 1
    elif stage == 3:
        mail = message.text
        await message.answer(Resources.NICKNAME)
        stage += 1
    elif stage == 4:
        nickname = message.text
        await message.answer(Resources.CITY)
        stage += 1
    elif stage == 5:
        city = message.text
        await message.answer(Resources.AGE)
        stage += 1
    elif stage == 6:
        age = message.text
        await message.answer(Resources.GRADE)
        stage += 1
    elif stage == 7:
        grade = message.text
        await message.answer(Resources.SCHOOL)
        stage += 1
    elif stage == 8:
        school = message.text
        await message.answer(Resources.REGISTRATION_COMPLETE)
        stage += 1


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

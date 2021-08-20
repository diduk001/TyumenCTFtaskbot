from resources import Resources
from config import Config
from aiogram import Bot, Dispatcher, types, executor
from models import User, findUserChatID, session

bot = Bot(Config.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start_cmd_handler(message: types.Message):
    if findUserChatID(message.chat.id):
        await message.answer(Resources.SIGNED_UP)
    else:
        u = User(chatId=message.chat.id)

        u.name = ""
        u.surname = ""
        u.email = ""
        u.nickname = ""
        u.age = 0
        u.city = ""
        u.school = ""
        u.grade = 0
        u.signUpStage = 1

        u.signUpUser()

        await message.answer(Resources.START)
        await message.answer(Resources.NAME)


@dp.message_handler(commands="kill")
async def kill_cmd_handler(message: types.Message):
    cur_user = findUserChatID(message.chat.id)

    if not cur_user:
        await message.answer(Resources.NOT_SIGNED_UP)
    else:
        cur_user.deleteUser()
        await message.answer(Resources.KILLED_SUCCESS)


@dp.message_handler()
async def msg_handler(message: types.Message):
    cur_user = findUserChatID(message.chat.id)
    # пользователя нет в БД
    if not cur_user:
        await message.answer(Resources.NOT_SIGNED_UP)
    else:
        stg = cur_user.signUpStage
        msg_text = message.text

        if stg == 1:
            cur_user.name = msg_text
            await message.answer(Resources.SURNAME)
        elif stg == 2:
            cur_user.surname = msg_text
            await message.answer(Resources.EMAIL)
        elif stg == 3:
            cur_user.email = msg_text

            # We need to validate email here

            await message.answer(Resources.NICKNAME)
        elif stg == 4:
            cur_user.nickname = msg_text
            await message.answer(Resources.CITY)
        elif stg == 5:
            cur_user.city = msg_text
            await message.answer(Resources.AGE)
        elif stg == 6:
            cur_user.age = int(msg_text)

            # We need to validate age here

            await message.answer(Resources.GRADE)
        elif stg == 7:
            cur_user.grade = int(msg_text)

            # We need to validate grade here

            await message.answer(Resources.SCHOOL)
        elif stg == 8:
            cur_user.school = msg_text
            await message.answer(Resources.REGISTRATION_COMPLETE)
        if stg <= 8:
            cur_user.signUpStage += 1
            session.commit()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

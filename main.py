from aiogram import Bot, Dispatcher, types, executor
from aiogram.types.inline_keyboard import InlineKeyboardButton
from aiogram.utils.markdown import *

from resources import Resources
from config import Config

from models import *

bot = Bot(Config.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start_cmd_handler(message: types.Message):
    if findUserByChatID(message.chat.id):
        await message.answer(Resources.SIGNED_UP)
    else:
        u = User(chatId=message.chat.id)

        u.name = ""
        u.surname = ""
        u.admin = False
        u.banned = False
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
    cur_user = findUserByChatID(message.chat.id)

    if not cur_user:
        await message.answer(Resources.NOT_SIGNED_UP)
    elif cur_user.isBanned():
        await message.answer(Resources.BANNED)
    else:
        cur_user.deleteUser()
        await message.answer(Resources.KILLED_SUCCESS)


@dp.message_handler(commands=Config.ADMIN_PASS)
async def admin_login_handler(message: types.Message):
    cur_user = findUserByChatID(message.chat.id)
    if not cur_user:
        await message.answer(Resources.NOT_SIGNED_UP)
    elif cur_user.isBanned():
        await message.answer(Resources.BANNED)
    else:
        cur_user.toAdmin()
        await message.answer(Resources.ADMIN_SUCCESS)


@dp.message_handler(commands="tasks")
async def all_tasks_handler(message: types.Message):
    cur_user = findUserByChatID(message.chat.id)
    ctgs = getCategoriesSolvedAll(cur_user)

    kb_markup = types.InlineKeyboardMarkup(row_width=1)
    for category, solved, all in ctgs:
        btn_text = Resources.BTN_TXT_CATEGORY_FORMAT.format(
            category, solved, all)
        btn_callback = Resources.CATEGORY_CALLBACK_FORMAT.format(category)
        btn = InlineKeyboardButton(btn_text, callback_data=btn_callback)

        kb_markup.add(btn)
    await message.answer(Resources.CHOOSE_CATEGORY, reply_markup=kb_markup)


@dp.callback_query_handler()
async def task_and_category_handler(query: types.CallbackQuery):
    data = query.data
    callback_type = data.split("_")[0]

    if callback_type == "category":
        category = query.data.split("_")[1]
        await query.answer(Resources.CHOSEN_CATEGORY_FORMAT.format(category))

        cur_user = findUserByChatID(query.from_user.id)

        tasks = getTasksByCategory(category)
        kb_markup = types.InlineKeyboardMarkup(row_width=1)

        for t in tasks:
            btn_text = Resources.BTN_TXT_TASK_FORMAT.format(t.name, t.value)
            if solved(cur_user, t):
                btn_text = strikethrough(btn_text)
            btn_callback = Resources.TASK_CALLBACK_FORMAT.format(
                t.category, t.name)
            btn = InlineKeyboardButton(btn_text, callback_data=btn_callback)

            kb_markup.add(btn)
        await bot.send_message(
            query.from_user.id, Resources.CHOOSE_TASK, reply_markup=kb_markup
        )
    elif callback_type == "task":
        _, task_category, task_name = data.split("_")
        await query.answer(Resources.CHOSEN_TASK_FORMAT.format(task_name))

        task = getTaskByNameCategory(task_name, task_category)
        description = task.description
        value = task.value
        # TODO:
        # Inline submit flag button here
        await bot.send_message(
            query.from_user.id,
            Resources.TASK_DISPLAYING_FORMAT.format(
                task_name, value, description),
        )


@dp.message_handler()
async def msg_handler(message: types.Message):
    cur_user = findUserByChatID(message.chat.id)
    # пользователя нет в БД
    if not cur_user:
        await message.answer(Resources.NOT_SIGNED_UP)
    elif cur_user.isBanned():
        await message.answer(Resources.BANNED)
    elif cur_user.signUpStage <= 8:
        stg = cur_user.signUpStage
        msg_text = message.text
        success = True

        if stg == 1:
            cur_user.name = msg_text
            await message.answer(Resources.SURNAME)
        elif stg == 2:
            cur_user.surname = msg_text
            await message.answer(Resources.EMAIL)
        elif stg == 3:
            if not Config.MAIL_REGEX.match(msg_text):
                success = False
                await message.answer(Resources.EMAIL_INVALID)
                await message.answer(Resources.NEW_EMAIL)
            else:
                cur_user.email = msg_text
                await message.answer(Resources.NICKNAME)
        elif stg == 4:
            cur_user.nickname = msg_text
            await message.answer(Resources.CITY)
        elif stg == 5:
            cur_user.city = msg_text
            await message.answer(Resources.AGE)
        elif stg == 6:
            if not Config.DIGITS_REGEX.match(msg_text):
                success = False
                await message.answer(Resources.AGE_INVALID)
                await message.answer(Resources.NEW_AGE)
            else:
                cur_user.age = int(msg_text)
                await message.answer(Resources.GRADE)
        elif stg == 7:
            if not Config.DIGITS_REGEX.match(msg_text):
                success = False
                await message.answer(Resources.GRADE_INVALID)
                await message.answer(Resources.NEW_GRADE)
            else:
                cur_user.grade = int(msg_text)
                await message.answer(Resources.SCHOOL)
        elif stg == 8:
            cur_user.school = msg_text
            await message.answer(Resources.REGISTRATION_COMPLETE)

        if success:
            cur_user.signUpStage += 1
            session.commit()


if __name__ == "__main__":
    randTasks(25)
    executor.start_polling(dp, skip_updates=True)

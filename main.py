from resources import Resources
from config import Config

from aiogram import Bot, Dispatcher, executor, types

bot = Bot(Config.BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message):
    await message.reply(Resources.START_MSG)

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text[::-1])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
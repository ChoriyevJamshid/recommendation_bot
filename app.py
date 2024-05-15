import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv, find_dotenv
from djapp.tasks import get_parsing_data

load_dotenv(find_dotenv())

from database.engine import create_db, drop_db

bot = Bot(token=os.getenv('TOKEN'), parse_mode='HTML')

dp = Dispatcher()


async def on_startup(bot):
    run_param = False
    if run_param:
        await drop_db()

    await create_db()


@dp.message(CommandStart())
async def command_start(message: types.Message):
    return await message.answer("<b>Assalomu alaykum!</b>")


@dp.message(Command('parse'))
async def command_parse(message: types.Message):
    await message.answer("Parsing started!")
    get_parsing_data.delay()
    return await message.answer("Parsing finished!")


async def main():
    print("Bot starting...")
    dp.startup.register(on_startup)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

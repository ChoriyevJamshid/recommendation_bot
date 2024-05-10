import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('TOKEN'),
          parse_mode=ParseMode.HTML)

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start(message: types.Message):
    return await message.answer("<b>Assalomu alaykum!</b>")


async def main():
    print("Bot starting...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

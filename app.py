import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djconfig.settings')
django.setup()

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv, find_dotenv
from asgiref.sync import sync_to_async
from djapp.models import Product

load_dotenv(find_dotenv())



bot = Bot(token=os.getenv('TOKEN'), parse_mode=ParseMode.HTML)

dp = Dispatcher()


async def on_startup():
    print('Bot started...')


@dp.message(CommandStart())
async def command_start(message: types.Message):
    return await message.answer("<b>Assalomu alaykum!</b>")


@dp.message(Command('products'))
async def command_parse(message: types.Message):
    products = await sync_to_async(lambda: list(Product.objects.all()[:10]))()
    text = 'Products\n'
    print(products)
    for product in products:
        title = product.title
        text += f"<b>{title}\n</b>"
    return await message.answer(text)


async def main():
    dp.startup.register(on_startup)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

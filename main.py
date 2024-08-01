import asyncio
import logging

from config_reader import config
import db, kb
import handlers

from aiogram import Bot, Dispatcher

bot = Bot(token = config.bot_token.get_secret_value())
dp = Dispatcher()

async def main():
    logging.basicConfig(level=logging.INFO)

    await db.creat_table_products()
    await db.creat_table_reservating()

    dp.include_router(handlers.rout)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
        
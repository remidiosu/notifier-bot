from bot.logger_config import setup_logger

setup_logger()

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot.db import init_db
from dotenv import load_dotenv

from bot.checker import check_site
from bot.cmds import router, start_periodic_check

import os

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(router)


async def main():
    await init_db()
    asyncio.create_task(start_periodic_check(bot))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from bot.handlers import router

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

if API_TOKEN is None:
    raise ValueError("API_TOKEN environment variable is not set.")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


dp.include_router(router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

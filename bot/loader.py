from aiogram import Bot, Dispatcher
from utils.load_env import TOKEN
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.handlers.aps_task import aps_task_message

bot = Bot(token=TOKEN)
dp = Dispatcher()

scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
scheduler.add_job(aps_task_message, trigger='interval', minutes=5, kwargs={'bot': bot})

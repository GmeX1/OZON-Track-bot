import asyncio

from loguru import logger
import sys
from bot.loader import dp, bot, scheduler
from bot.handlers import routers

logger.remove()
logger.add(sys.stderr, level='DEBUG', enqueue=True, colorize=True)
logger.add('ozon_log.log', level='DEBUG', enqueue=True, retention='30 days')

dp.include_routers(*routers)
# TODO: README + DOCKER README

async def main():
    try:
        logger.info('Запускаю scheduler...')
        scheduler.start()
        logger.info('Запускаю бота...')
        await dp.start_polling(bot)
    except Exception as ex:
        logger.error(f'Ошибка при выполнении: {ex}')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info('Останавливаю работу...')

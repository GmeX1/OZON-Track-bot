from aiogram import Bot
from utils.load_env import TG_ID
from ozon_fetch.delivery_class import DeliveryStatusManager
from ozon_fetch.ozon_fetch import get_delivery_status
from loguru import logger

ozon_mng = DeliveryStatusManager()


async def aps_task_message(bot: Bot):
    status = await get_delivery_status()
    result = await ozon_mng.pull_changes(status)

    if result:
        logger.info('Найдены изменения в доставке!')
        await bot.send_message(TG_ID, result)
    else:
        logger.debug('Изменений в доставке не найдено...')

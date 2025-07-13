import aiohttp
from datetime import datetime
from utils.load_env import TRACK_ID
from .delivery_class import DeliveryStatus


async def get_delivery_status():
    headers = {
        'Accept': 'application/json'
    }
    url = f'https://tracking.ozon.ru/p-api/ozon-track-bff/tracking/{TRACK_ID}?source=Global'

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers) as response:
            match response.status:
                case 200:
                    content = await response.json()
                    # print(content)
                    items = content.get('items', '')
                    if items:
                        last_event = items[-1]
                        event = last_event.get('event', '')

                        event_time = datetime.strptime(last_event.get('moment', ''), '%Y-%m-%dT%H:%M:%S.%f%z')
                        period = datetime.strptime(content.get('deliveryDatePeriodChangedMoment', ''),
                                                   '%Y-%m-%dT%H:%M:%S.%f%z')
                        endtime = datetime.strptime(content.get('deliveryDateEnd', ''), '%Y-%m-%dT%H:%M:%S%z')

                        return DeliveryStatus(
                            item=(event, event_time),
                            period=period,
                            endtime=endtime
                        )

                    else:
                        return DeliveryStatus(
                            exception='\n'.join(['Ошибка JSON. Не удалось получить этапы заказа:', content]))
                case _:
                    return DeliveryStatus(exception='\n'.join([f'Ошибка {response.status}!', await response.text()]))

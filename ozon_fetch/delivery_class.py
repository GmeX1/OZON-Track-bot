from datetime import datetime, timezone, timedelta
from utils.translator import translate


class DeliveryStatus:
    def __init__(self, item: tuple[str, datetime] = None, period: datetime = None, endtime: datetime = None,
                 exception: str = None):
        self.item = item
        self.period = period
        self.endtime = endtime
        self.exception = exception
        if (exception is None) and any(filter(lambda x: x is None, [item, period, endtime])):
            raise Exception('Status is improperly filled or exception is not set!')


class DeliveryStatusManager(DeliveryStatus):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, exception='Manager')

    def overwrite_changes(self, status: DeliveryStatus):
        self.item = status.item
        self.period = status.period
        self.endtime = status.endtime

    async def pull_changes(self, status: DeliveryStatus):
        if status.exception is not None:
            return status.exception

        if status.item != self.item:
            self.overwrite_changes(status)

            time_local = self.item[1].astimezone(timezone(offset=timedelta(hours=3)))
            translated = await translate(self.item[0])

            return '\n'.join((
                'Обнаружены изменения в доставке!', '',
                f'Статус доставки: {translated} ({self.item[0]})',
                f'Дата изменений: {time_local.strftime('%d.%m.%Y %H:%M:%S')}'
            ))

        if status.period != self.period or status.endtime != self.endtime:
            old_time = self.endtime
            self.overwrite_changes(status)
            period_local = self.period.astimezone(timezone(offset=timedelta(hours=3)))

            return '\n'.join((
                'Обнаружены изменения в дате доставки!', '',
                f'Старое время доставки: {old_time}',
                f'Новое время доставки: {status.endtime}',
                f'Дата изменений: {period_local.strftime('%d.%m.%Y %H:%M:%S')}'
            ))
        return None

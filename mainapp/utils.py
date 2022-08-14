from typing import Union

from django.utils.timezone import datetime


class DateUtil:
    def __init__(self, date: Union[datetime, str, None]) -> None:
        self.date = date

    def format_date_to_str(self) -> Union[str, None]:
        return self.date.strftime("%d.%m.%Y, %H:%M:%S") if self.date else None

    def format_str_to_date(self) -> Union[datetime, None]:
        return datetime.strptime(self.date, "%Y-%m-%d") if self.date else None

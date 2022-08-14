from typing import Union

from django.utils.timezone import datetime


def format_date(date: Union[datetime, None]) -> Union[str, None]:
    return date.strftime("%d.%m.%Y, %H:%M:%S") if date else None

import datetime

DATE_FORMAT = "%Y-%m-%d"
DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"


def get_formatted_date(
    date_to_format: datetime.date,
    date_format: str = DATE_FORMAT,
):
    """Возвращает форматированную дату"""
    return date_to_format.strftime(date_format)


def get_formatted_datetime(
    datetime_to_format: datetime.datetime,
    date_format: str = DATE_TIME_FORMAT,
):
    """Возвращает форматированную дату-время"""
    return datetime_to_format.strftime(date_format)

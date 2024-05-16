import calendar
import datetime

from dateutil.relativedelta import relativedelta


def last_day_of_relative_month_str(x: datetime.datetime, steps: int) -> str:
    y = x + relativedelta(months=steps)
    _, last = calendar.monthrange(y.year, y.month)
    return datetime.datetime(y.year, y.month, last).strftime("%Y-%m-%d")

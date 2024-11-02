import arrow
import time


def time_to_text(_time: arrow.Arrow, auto_granularity: bool = True, **kwargs) -> str:
    if auto_granularity:
        now = arrow.now()
        diff = (now - _time).total_seconds()
        if diff >= 31536000:  # more than a year
            granularity = ['year', 'month']
        elif diff >= 2592000:  # more than a month
            granularity = ['month', 'week']
        elif diff >= 604800:  # more than a week
            granularity = ['week', 'day']
        elif diff >= 86400:  # more than a day
            granularity = ['day', 'hour']
        elif diff >= 3600:  # more than an hour
            granularity = ['hour', 'minute']
        else:
            granularity = ['minute', 'second']
    else:
        granularity = [unit for unit, include in kwargs.items() if include]

    if not granularity:
        return _time.humanize()
    return _time.humanize(granularity=granularity)


def current_time():
    time = arrow.now()
    return time


# Example usage
print(current_time())
print(time_to_text(current_time()))
print(time_to_text(arrow.get("2021-01-01")))
print(time_to_text(arrow.get("2024-11-2").shift(hours=-5)))

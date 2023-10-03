from datetime import datetime, timedelta


def get_next_datetime(scheduled_time):
    time_now = datetime.now().time()
    scheduled_day = datetime.now().date()
    if time_now > scheduled_time:
        scheduled_day += timedelta(days=1)
    scheduled_datetime = datetime.combine(scheduled_day, scheduled_time)
    return scheduled_datetime

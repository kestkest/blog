import pytz
from datetime import datetime


def format_date(dt, formate=None):
    if dt is None:
        return ""
    if formate is None:
        formatted_date = dt.strftime("%Y-%m-%d")
        formatted_time = dt.strftime("%I:%M%p").lstrip('0').lower()
        formatted = "%s at %s" % (formatted_date, formatted_time)
    else:
        formatted = dt.strftime(formate)
    return formatted


def show_time_passed(past):
    past = past.replace(tzinfo=None)
    present = datetime.now()
    margin = present - past
    minutes = int(divmod(margin.total_seconds(), 60)[0])
    hours = int(minutes / 60)
    days = int(hours / 24)

    if days:
        return "{} day(s) ago".format(days)
    if hours:
        return "{} hour(s) ago".format(hours)
    if minutes < 60:
        return "{} minute(s) ago".format(minutes)




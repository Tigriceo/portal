from datetime import datetime, timezone, timedelta

from django import template


register = template.Library()


def padegi(var=0, arg="дурак,дурака,дураков"):
    """Падежи"""

    args = arg.split(",")
    a = var % 10
    b = var % 100

    if (a == 1) and (b != 11):
        return "{} {}".format(var, args[0])
    elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
        return "{} {}".format(var, args[1])
    else:
        return "{} {}".format(var, args[2])


@register.filter()
def delta(value):
    """Актуально Х дней и Х часов"""

    delta_date = value - datetime.now(timezone.utc)
    date = abs(delta_date)
    day = date.days
    hour = date.seconds // 3600
    if day <= 2:
        return 'quickly'
    else:
        return "{} {}".format(padegi(day, "день,дня,дней"), padegi(hour, "час,часа,часов"))


# @register.simple_tag
# def tomorrow(format):
#     tomorrow = (datetime.now() + timedelta(days=1))
#     print(tomorrow.strftime(format))
#     return tomorrow.strftime(format)
# {% tomorrow "%d.%m.%Y" %}

from django import template
import datetime

register = template.Library()


@register.simple_tag
def valid_days(valid_until):
    if valid_until is None:
        return 0
    d0 = datetime.date.today()
    d1 = valid_until
    delta = d1 - d0
    return(delta.days)

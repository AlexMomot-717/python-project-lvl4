from datetime import datetime

from django import template

register = template.Library()


@register.filter(name="format_datetime")
def format_datetime(value: datetime, format: str = "%d.%m.%Y %H:%M") -> str:
    """
    Takes a datetime object and formats it according to the given format string.
    """
    return value.strftime(format)

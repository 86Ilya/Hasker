from django import template
from django.utils import timezone

register = template.Library()


@register.filter(name='add_class')
def add_class(value, arg):
    return value.as_widget(attrs={'class': arg})


@register.filter(name='get_due_date_string')
def get_due_date_string(value):
    now = timezone.now()
    delta = now - value
    if delta.days >= 1:
        return "{} days ago".format(delta.days)
    else:
        if delta.seconds < 60:
            return "{} seconds ago".format(delta.seconds)
        if 60 < delta.seconds < 60 * 60:
            return "{} minutes ago".format(delta.seconds // 60)

        return "{} hours ago".format(delta.seconds // (60 * 60))

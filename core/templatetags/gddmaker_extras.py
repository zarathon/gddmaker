from django import template
from core.models import Character, Mechanic, Media

register = template.Library()


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_character(value):
    return Character.objects.get(id=value)


@register.filter
def get_mechanic(value):
    return Mechanic.objects.get(id=value)


@register.filter
def get_media(value):
    return Media.objects.get(id=value)

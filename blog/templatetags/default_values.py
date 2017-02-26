from django import template
from django import forms

register = template.Library()

@register.filter
def default_choice(field, choice):
    if choice:
        choice_id = 0
        for e in field.field.choices:
            if e[0] == choice:
                choice_id = e[0]

        field.field.initial = choice_id
    return field

@register.filter
def default_value(field, value):
    if value:
        field.field.initial= value
    return field

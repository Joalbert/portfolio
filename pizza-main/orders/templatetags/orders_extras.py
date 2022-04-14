from django import template
from ..models import Menu
register = template.Library()

@register.filter()
def meal_size(meal_size_id):
    return Menu.SIZE[int(meal_size_id)-1][1]

@register.filter()
def meal_name(meal_id):
    return Menu.MEAL_TYPE[int(meal_id)-1][1]

@register.filter()
def total(orders):
    total = 0
    for order in orders:
        total += order.total
    return total

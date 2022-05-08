from django import template
from orders.models import Pizza, Sub, DinnerPlatter
register = template.Library()

@register.filter()
def meal_size(meal_size_id):
    return Pizza.SIZE[int(meal_size_id)][1]

@register.filter()
def sub_meal_size(size):
    return Sub.SIZE[int(size)-1][1]

@register.filter()
def dinner_size(size):
    return DinnerPlatter.SIZE[int(size)][1]


@register.filter()
def meal_name(meal_id):
    return Pizza.MEAL_TYPE[int(meal_id)-1][1]

@register.filter()
def total(orders):
    total = 0
    for order in orders:
        total += order.total
    return total

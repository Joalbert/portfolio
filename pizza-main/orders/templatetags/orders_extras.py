import enum
from django import template

from orders.models import Pizza, Sub, DinnerPlatter
from orders.helpers import (is_pizza, is_salad, is_sub, is_salad, 
                            is_pasta, is_dinner)

register = template.Library()

@register.filter()
def meal_size(meal_size_id):
    return Pizza.SIZE[int(meal_size_id)][1]

@register.filter()
def sub_meal_size(size):
    return Sub.SIZE[int(size)][1]

@register.filter()
def dinner_size(size):
    return DinnerPlatter.SIZE[int(size)][1]


@register.filter()
def get_pizza_type(meal_id):
    return Pizza.MEAL_TYPE[int(meal_id)][1]

@register.filter()
def total(orders):
    total = 0
    for order in orders:
        total += order.total
    return total

@register.filter()
def food_desc(item):
    text = ""
    if(is_pizza(item.menu)):
        text += f"{Pizza.MEAL_TYPE[item.menu.pizza.meal_type][1]} {item.menu.ingredient}"
        queryset = item.toppings.all()
        max_top = len(queryset)
        for index, top in enumerate(queryset):
            if index==0:
                text += "Toppings: "
            text += f"{top.topping}" 
            if index+1<max_top:
                text += ", "
        return text
    if (is_sub(item.menu)): 
        text += f"Sub {item.menu.ingredient}"
        queryset = item.extra.all()
        extras_items = len(queryset)
        for index, top in enumerate(queryset):
            if index==0:
                text += "Toppings: "
            text += f"{top.extra}" 
            if index+1<extras_items:
                text += ", "
        return text
    if(is_salad(item.menu)):
        return f"Salad {item.menu.ingredient}"

    if(is_pasta(item.menu)):
        return f"Pasta {item.menu.ingredient}"
    
    if(is_dinner(item.menu)):
        return f"Dinner Platter {item.menu.ingredient}"


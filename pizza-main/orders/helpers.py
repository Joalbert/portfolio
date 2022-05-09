from orders.models import (Pizza, Menu, Sub)

def is_pizza(food):
    try:
        if isinstance(food.pizza,Pizza):
            return True
        return False
    except Menu.pizza.RelatedObjectDoesNotExist:
        return False

def is_sub(food):
    try:
        if isinstance(food.sub,Sub):
            return True
        return False
    except Menu.sub.RelatedObjectDoesNotExist:
        return False

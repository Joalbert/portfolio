from orders.models import (Pizza, Menu, Sub, Salad, Pasta, DinnerPlatter)

def is_pizza(food):
    try:
        return isinstance(food.pizza,Pizza)
    except Menu.pizza.RelatedObjectDoesNotExist:
        return False

def is_sub(food):
    try:
        return isinstance(food.sub,Sub)
    except Menu.sub.RelatedObjectDoesNotExist:
        return False

def is_salad(food):
    try:
        return isinstance(food.salad,Salad)
    except Menu.salad.RelatedObjectDoesNotExist:
        return False

def is_pasta(food):
    try:
        return isinstance(food.pasta,Pasta)
    except Menu.pasta.RelatedObjectDoesNotExist:
        return False

def is_dinner(food):
    try:
        return isinstance(food.dinnerplatter,DinnerPlatter)
    except Menu.dinnerplatter.RelatedObjectDoesNotExist:
        return False
    
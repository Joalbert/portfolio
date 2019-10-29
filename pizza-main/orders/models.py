from django.db import models
from django.contrib.auth.models import User


class Ingredient(models.Model):
    ingredient = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.ingredient}"

class Extra(models.Model):
    extra = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    def __str__(self):
        return f"{self.extra}"


class Topping(models.Model):
    topping = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.topping}"


class Order(models.Model):
    STATUS=((1,"Open"), (2, "Done"))
    order_total = models.FloatField(default=0)
    order_date = models.DateField(blank=True)
    status = models.PositiveSmallIntegerField(choices=STATUS, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="OrderUser")

    def __str__(self):
        return f"Order Number: {self.id} " \
               f"Order Date: {self.order_date}  " \
               f"Order Total: {self.order_total} "


class Menu(models.Model):
    SIZE = ((1,"Small"), (2,"Large"), (3, "Standard"))
    MEAL_TYPE = ((1,"Regular Pizza"),(2,"Sicilian Pizza"), (3, "Sub"), (4, "Pasta"), (5, "Salad"), (6, "Dinner Platter"))
    meal_type = models.PositiveSmallIntegerField(choices=MEAL_TYPE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="Ingredients")
    meal_size = models.PositiveSmallIntegerField(choices=SIZE)
    photo = models.ImageField(upload_to='food-img/', default = 'food-img/None/no-img.jpg')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    topping_flag = models.BooleanField(default=False)
    extras_flag = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.meal_type} {self.meal_size} {self.ingredient} ${self.price} "


class Order_Status(models.Model):
    STATUS=((1,"Open"), (2, "Done"))
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True,
                                 null=True,
                                 related_name="Order")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="User")
    menu_id = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="Menu")
    quantity = models.IntegerField(default=0)
    status = models.PositiveSmallIntegerField(choices=STATUS)
    extras = models.CharField(max_length=256, blank=True)
    topping = models.CharField(max_length=256, blank=True)
    total = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.order_id} {self.user_id} {self.menu_id} {self.status} " \
               f"{self.quantity} {self.extras} {self.topping} {self.total}"

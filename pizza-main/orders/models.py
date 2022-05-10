from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError

class Extra(models.Model):
    extra = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f"{self.extra}"


class Topping(models.Model):
    topping = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.topping}"

class Menu(models.Model):
    photo = models.ImageField(upload_to='food-img/', default = 'food-img/None/no-img.jpg')
    ingredient = models.CharField(max_length=64, default="")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f"{self.ingredient}"

class Pizza(Menu):
    SIZE = ((0,"Small"), (1,"Large"),)
    MEAL_TYPE = ((0,"Regular Pizza"),(1,"Sicilian Pizza"),)
    AMOUNT_TOPPINGS = ((0,0),(1,1),(2,2),(3,3))
    meal_type = models.PositiveSmallIntegerField(choices=MEAL_TYPE)
    meal_size = models.PositiveSmallIntegerField(choices=SIZE)
    amount_toppings = models.PositiveSmallIntegerField(choices=AMOUNT_TOPPINGS,default=0)

    def __str__(self):
        return (
            f"{self.MEAL_TYPE[self.meal_type][1]} " 
            f"{self.ingredient} "
            f"{self.SIZE[self.meal_size][1]} "
            )
    
    

class Sub(Menu):
    SIZE = ((0,"Small"), (1,"Large"),)
    meal_size = models.PositiveSmallIntegerField(choices=SIZE)

    def __str__(self):
        return (
            f"{self.ingredient} "
            f"{self.SIZE[self.meal_size][1]} "
        )
            
    
class Salad(Menu):
    
    def __str__(self):
        return f"{self.ingredient}"
            
    
class Pasta(Menu):
    
    def __str__(self):
        return f"{self.ingredient}"
            
    
class DinnerPlatter(Menu):
    SIZE = ((0,"Small"), (1,"Large"),)
    meal_size = models.PositiveSmallIntegerField(choices=SIZE)

    def __str__(self):
        return f"{self.ingredient}"
            


class Order(models.Model):
    STATUS=((0,"Draft, in cart"), (1, "Placed, release by client"), 
            (2, "Cooked"), (3, "Deliveried"), 
            (4, "Canceled"), (5, "Paid"),)
    STATUS_DRAFT = 0
    order_total = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=STATUS, default=STATUS_DRAFT)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, 
                            related_name="OrderUser", null=True, blank=True)

    def __str__(self):
        return f"Order Number: {self.id} "               
    
    def get_absolute_url(self):
        return reverse("orders:invoices")
    

class Cart(models.Model):
    STATUS=((0,"Open"), (1, "Release"))
    STATUS_OPEN = 0
    INITIAL_QTY = 0
    INITIAL_COST = 0 
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True,
                                 related_name="CartOrder")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Cart_User")
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="Cart_Menu")
    quantity = models.IntegerField(default=INITIAL_QTY)
    status = models.PositiveSmallIntegerField(choices=STATUS, default=STATUS_OPEN)
    sub_total_item = models.DecimalField(max_digits=6, decimal_places=2, 
                                        default=INITIAL_COST)
    toppings = models.ManyToManyField(Topping, related_name="CartTopping", blank=True)
    extra = models.ManyToManyField(Extra, related_name="CartExtra", blank=True)
    
    def __str__(self):
        return f"{self.order} {self.user} {self.menu} {self.status} " \
               f"{self.quantity} {self.extra} {self.toppings} "

    def get_absolute_url(self):
        return reverse("orders:cart")

    def clean(self):
        if self.quantity<0:
            raise ValidationError({'quantity':["It should be bigger than zero!",]})
        if self.sub_total_item<0:
            raise ValidationError({'sub_total_item':["It should be bigger than zero!",]})
        return super().clean()
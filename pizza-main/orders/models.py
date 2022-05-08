from string import digits
from django.db import models
from django.contrib.auth.models import User

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
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f"{self.price}"

class Pizza(Menu):
    SIZE = ((0,"Small"), (1,"Large"),)
    MEAL_TYPE = ((0,"Regular Pizza"),(1,"Sicilian Pizza"),)
    AMOUNT_TOPPINGS = ((0,0),(1,1),(2,2),(3,3))
    meal_type = models.PositiveSmallIntegerField(choices=MEAL_TYPE)
    ingredient = models.CharField(max_length=64)
    meal_size = models.PositiveSmallIntegerField(choices=SIZE)
    amount_toppings = models.PositiveSmallIntegerField(choices=AMOUNT_TOPPINGS,default=0)

    def __str__(self):
        return (
            f"{self.MEAL_TYPE[self.meal_type][1]} " 
            f"{self.ingredient}"
            )
    
    

class Sub(Menu):
    SIZE = ((1,"Small"), (2,"Large"),)
    ingredient = models.CharField(max_length=64)
    meal_size = models.PositiveSmallIntegerField(choices=SIZE)

    def __str__(self):
        return f"{self.ingredient}"
            
    
class Salad(Menu):
    ingredient = models.CharField(max_length=64)
    
    def __str__(self):
        return f"{self.ingredient}"
            
    
class Pasta(Menu):
    ingredient = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.ingredient}"
            
    
class DinnerPlatter(Menu):
    SIZE = ((0,"Small"), (1,"Large"),)
    ingredient = models.CharField(max_length=64)
    meal_size = models.PositiveSmallIntegerField(choices=SIZE)

    def __str__(self):
        return f"{self.ingredient}"
            


class Order(models.Model):
    STATUS=((0,"In Chart"), (1, "Paid"), (2, "Cooking"), (3, "Deliveried"), (4, "Canceled"))
    order_total = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.PositiveSmallIntegerField(choices=STATUS, default=1)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, 
                            related_name="OrderUser", null=True, blank=True)

    def __str__(self):
        return f"Order Number: {self.id} " \
               f"Order Date: {self.order_date}  " \
               f"Order Total: {self.order_total} "

class Chart(models.Model):
    STATUS=((0,"Open"), (1, "Release"), (2, "Canceled"))
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True,
                                 related_name="Order")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Chart_User")
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="Chart_Menu")
    quantity = models.IntegerField(default=0)
    status = models.PositiveSmallIntegerField(choices=STATUS)
    sub_total_item = models.DecimalField(max_digits=6, decimal_places=2)
    toppings = models.ManyToManyField(Topping, related_name="ChartTopping")
    extra = models.ManyToManyField(Topping, related_name="ChartExtra")
    def __str__(self):
        return f"{self.order_id} {self.user_id} {self.menu_id} {self.status} " \
               f"{self.quantity} {self.extras} {self.topping} {self.total}"

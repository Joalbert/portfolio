from django.contrib import admin

# Register your models here.
from orders.models import *

class FoodAdmin(admin.ModelAdmin):
    list_display = ("id","ingredient","price")
    list_editable=("ingredient","price")

class CartAdmin(admin.ModelAdmin):
    list_display = ("id","menu", "user", "order","status")
    list_editable = ("status",)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id","status", "user")
    list_editable =("status", "user")

admin.site.register(Extra)
admin.site.register(Topping)
admin.site.register(Menu)
admin.site.register(Pizza, FoodAdmin)
admin.site.register(Sub, FoodAdmin)
admin.site.register(Salad, FoodAdmin)
admin.site.register(DinnerPlatter, FoodAdmin)
admin.site.register(Pasta, FoodAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)

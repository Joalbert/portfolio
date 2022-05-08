from django.contrib import admin

# Register your models here.
from orders.models import *

admin.site.register(Extra)
admin.site.register(Topping)
admin.site.register(Menu)
admin.site.register(Pizza)
admin.site.register(Sub)
admin.site.register(Salad)
admin.site.register(DinnerPlatter)
admin.site.register(Pasta)
admin.site.register(Chart)
admin.site.register(Order)

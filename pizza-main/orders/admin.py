from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Ingredient)
admin.site.register(Topping)
admin.site.register(Menu)
admin.site.register(Extra)
admin.site.register(Order_Status)
admin.site.register(Order)

from audioop import reverse
from re import template
from django.shortcuts import redirect
from django.urls import path, reverse_lazy
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import MenuView, Register,Cart, Invoice

from django.contrib.auth.views import LoginView, LogoutView
app_name = "orders"

urlpatterns = [
    path("login/", LoginView.as_view(template_name = "orders/login.html"), 
                                    name = "login"),
    path("logout/", LogoutView.as_view(template_name = "orders/logout.html"), 
                                    name="logout"),
    path("register/", Register.as_view(), name="register"),
    
    path("", MenuView.as_view(), name="index"),
    path("cart/", Cart.as_view(), name="cart"),
    path("invoices/", Invoice.as_view(), name="invoices"),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

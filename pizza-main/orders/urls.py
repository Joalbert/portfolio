from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

from orders.views import (MenuView, Register,CartView,
        AddItemCartView, UpdateItemCartView, DeleteItemCartView,
        OrderView, UpdateOrderView)

app_name = "orders"

urlpatterns = [
    path("login/", LoginView.as_view(template_name = "orders/login.html"), 
                                    name = "login"),
    path("logout/", LogoutView.as_view(template_name = "orders/logout.html"), 
                                    name="logout"),
    path("register/", Register.as_view(), name="register"),
    
    path("", MenuView.as_view(), name="index"),
    
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/<int:menu>/", AddItemCartView.as_view(), name="addcart"),
    path("cart/<int:pk>/update", UpdateItemCartView.as_view(), name="updatecart"),
    path("cart/<int:pk>/delete", DeleteItemCartView.as_view(), name="deletecart"),
    path("orders/", OrderView.as_view(), name="invoices"),
    path("orders/<int:pk>/update", UpdateOrderView.as_view(), name="updateinvoices"),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

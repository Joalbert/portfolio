from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import MenuView, OrderFood, Register,Cart, Invoice, EditOrder, OrderTable

urlpatterns = [
    path("", MenuView.as_view(), name="index"),
    path("food/<int:meal>/<int:ingredient_desc>", OrderFood.as_view(), name="food"),
    path("cart/order/<int:order_status>", EditOrder.as_view(), name="edit-order"),
    path("price/<int:meal>/<int:ingredient>/<int:size>", views.food_price, name="price"),
    path("register", Register.as_view(), name="register"),
    path("cart/", Cart.as_view(), name="cart"),
    path("invoices/order-table/<int:order>", OrderTable.as_view(), name="order-table"),
    path("invoices/", Invoice.as_view(), name="invoices"),
    path("login_view", views.login_form, name="login_view"),
    path("logout_view", views.logout_form, name="logout_view"),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

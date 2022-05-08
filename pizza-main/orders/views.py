from typing import Dict, Any 

from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.models import User

from orders.forms import (UserForm, OrderForm)
from orders.models import (Sub, Pizza, Pasta, Salad, DinnerPlatter, 
                        Menu, Extra, Topping, Chart, Order)

#-------------------------------------------
#               Views
#-------------------------------------------
class MenuView(LoginRequiredMixin, ListView):
    template_name = "orders/menu.html"
    queryset = Menu
    context_object_name = "menu"
    login_url = reverse_lazy("orders:login")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        REGULAR_PIZZA = 0
        SICILIAN_PIZZA = 1

        context = super().get_context_data(**kwargs)
        context["regular_pizzas"] = Pizza.objects.filter(meal_type=REGULAR_PIZZA)
        context["sicilian_pizzas"] = Pizza.objects.filter(meal_type=SICILIAN_PIZZA) 
        context["subs"] = Sub.objects.all()  
        context["salads"] = Salad.objects.all()
        context["pastas"] = Pasta.objects.all()
        context["dinner_platters"] = DinnerPlatter.objects.all()
        context["toppings"] = Topping.objects.all()
        context["extras"] = Extra.objects.all()

        return context

class Register(CreateView):
    template_name = 'orders/register.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy("orders:index")

class Cart(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('orders:login')
    template_name = "orders/shopping_cart.html"

    def get_queryset(self):
        STATUS_OPEN = 0
        STATUS_RELEASE = 1
        STATUS_CANCELLED = 2  
        return Chart.objects.filter(Q(user=self.request.user)&~Q(status=STATUS_CANCELLED))

class Invoice(LoginRequiredMixin, ListView):
    login_url = 'register'
    template_name = "orders/invoices.html"
    paginate_by = 3

    def get_queryset(self):
        STATUS_PAID = 1
        return Order.objects.filter(status = STATUS_PAID, user_id = self.request.user)

class AddItemView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('orders:login')
    template_name = "orders/shopping_cart.html"

    def get_queryset(self):
        STATUS_OPEN = 0
        STATUS_RELEASE = 1
        STATUS_CANCELLED = 2  
        return Chart.objects.filter(Q(user=self.request.user)&~Q(status=STATUS_CANCELLED))

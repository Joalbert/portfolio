from telnetlib import STATUS
from typing import Dict, Any
from django.shortcuts import get_object_or_404

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.models import User

from orders.forms import (UserForm, CartForm, PizzaForm, SubForm)
from orders.models import (Sub, Pizza, Pasta, Salad, DinnerPlatter, 
                        Menu, Extra, Topping, Cart, Order)

class Register(CreateView):
    template_name = 'orders/register.html'
    model = User
    form_class = UserForm
    
    success_url = reverse_lazy("orders:index")

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

class AddItemCartView(LoginRequiredMixin, CreateView):
    template_name = "orders/form.html"
    login_url = reverse_lazy("orders:login")
    queryset = Cart
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =super().get_context_data(**kwargs)
        context["menu"] = Menu.objects.get(id=self.kwargs.get("menu",0))
        return context
    
    def get_initial(self) -> Dict[str, Any]:
        initial =super().get_initial()
        initial["menu"] = self.kwargs["menu"]
        return initial

    def get_form_class(self):
        food = get_object_or_404(Menu,pk=self.kwargs.get("menu",0))
        try:
            if isinstance(food.pizza,Pizza):
                return PizzaForm
        except Menu.pizza.RelatedObjectDoesNotExist:
            pass
        try:    
            if isinstance(food.sub,Sub):
                return SubForm
        except Menu.sub.RelatedObjectDoesNotExist:
            return CartForm    
 
class CartView(LoginRequiredMixin, ListView):
    template_name = "orders/shopping_cart.html"
    context_object_name = "carts"
    login_url = reverse_lazy("orders:login")

    def get_queryset(self):
        STATUS_OPEN = 0  
        return Cart.objects.filter(Q(user=self.request.user)&Q(status=STATUS_OPEN))

class UpdateItemCartView(LoginRequiredMixin, UpdateView):
    template_name = "orders/form.html"
    login_url = reverse_lazy("orders:login")
    STATUS_OPEN = 0
        
    def get_queryset(self):
        return Cart.objects.filter(Q(user=self.request.user)&Q(status=self.STATUS_OPEN))
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =super().get_context_data(**kwargs)
        cart = Cart.objects.get(id=self.kwargs.get("pk",0))
        context["menu"] = cart.menu
        return context

    def get_form_class(self):
        cart = get_object_or_404(Cart,pk=self.kwargs.get("pk",0))
        food = cart.menu
        try:
            if isinstance(food.pizza,Pizza):
                return PizzaForm
        except Menu.pizza.RelatedObjectDoesNotExist:
            pass
        try:    
            if isinstance(food.sub,Sub):
                return SubForm
        except Menu.sub.RelatedObjectDoesNotExist:
            return CartForm 

class DeleteItemCartView(LoginRequiredMixin, DeleteView):
    template_name = "orders/form.html"
    login_url = reverse_lazy("orders:login")
    form_class = CartForm
    success_url = reverse_lazy("orders:cart")
    
    def get_queryset(self):
        STATUS_OPEN = 0
        return Cart.objects.filter(Q(user=self.request.user)&Q(status=STATUS_OPEN))
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context =super().get_context_data(**kwargs)
        cart = Cart.objects.get(id=self.kwargs.get("pk",0))
        context["menu"] = cart.menu
        return context

class OrderView(LoginRequiredMixin, ListView):
    template_name = "orders/invoices.html"
    paginate_by = 3
    
    login_url = reverse_lazy("orders:login")

    def get_queryset(self):
        STATUS_DRAFT = 0
        return Order.objects.filter(~Q(status = STATUS_DRAFT) 
                    & Q(user_id = self.request.user))

class UpdateOrderView(LoginRequiredMixin, UpdateView):
    template_name = "orders/shopping_cart.html"
    login_url = reverse_lazy("orders:login")
    model = Order
    fields = ("id",)

    def get_queryset(self):
        STATUS_DRAFT = 0
        queryset = Order.objects.filter(Q(user=self.request.user)&
                        Q(status=STATUS_DRAFT) & 
                        Q(id=self.kwargs.get("pk",0)))
        return queryset
    
    def form_valid(self, form):
        STATUS_PLACE_ORDER = 1
        form.instance.status = STATUS_PLACE_ORDER 
        form.save()
        return super().form_valid(form)
        
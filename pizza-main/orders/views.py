from decimal import Decimal

from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages

from orders.forms import (UserForm, CartForm, PizzaForm, PizzaToppingsForm ,SubForm)
from orders.models import (Sub, Pizza, Pasta, Salad, DinnerPlatter, 
                        Menu, Extra, Topping, Cart, Order)
from orders.helpers import is_pizza, is_sub

class Register(CreateView):
    template_name = 'orders/register.html'
    model = User
    form_class = UserForm
    
    success_url = reverse_lazy("orders:index")

class MenuView(LoginRequiredMixin, TemplateView):
    template_name = "orders/menu.html"
    login_url = reverse_lazy("orders:login")

    def get_context_data(self, **kwargs):
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
    success_url = reverse_lazy("orders:cart")
    
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        context["menu"] = Menu.objects.get(id=self.kwargs.get("menu",0))
        context["title"] = "Add Item to Cart"
        return context
    
    def get_initial(self):
        initial =super().get_initial()
        initial["quantity"] = 1
        return initial

    def get_form_class(self):
        food = get_object_or_404(Menu,pk=self.kwargs.get("menu",0))
        if(is_pizza(food)):
            if food.pizza.amount_toppings==0:
                return PizzaForm
            return PizzaToppingsForm
        if (is_sub(food)):
            return SubForm
        return CartForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            STATUS_DRAFT = 0
            data = {k:v for k,v in request.POST.items()}
            # Preparing data
            data.pop("csrfmiddlewaretoken", 0)
            data.pop("toppings", 0)
            data.pop("extra", 0)
            
            # Complete fields for Cart
            data["menu"] = get_object_or_404(Menu,pk=self.kwargs.get("menu",0))
            data["user"] = self.request.user
            data["sub_total_item"] = Decimal(data["menu"].price) * Decimal(int(data["quantity"]))
            
            # Find order or create if not any in Draft status
            data["order"] , _ = Order.objects.get_or_create(user=self.request.user, 
                                        status = STATUS_DRAFT)

            # Check if food has toppings and if a valid option
            data_checkboxes = request.POST.copy() 
            toppings = data_checkboxes.pop("toppings",[])
            if(is_pizza(data["menu"])):
                if data["menu"].pizza.amount_toppings==0:
                    cart = Cart.objects.create(**data)
                    messages.add_message(request, messages.INFO, 
                                        f"¡{data['menu']} added!")
                    return HttpResponseRedirect(self.success_url)
                if len(toppings)==int(data["menu"].pizza.amount_toppings):
                    cart = Cart.objects.create(**data)
                    for top in toppings:
                        top_instance = Topping.objects.get(id=top)
                        cart.toppings.add(top_instance)
                    messages.add_message(request, messages.INFO, 
                                        f"¡{data['menu']} added!")
                    return HttpResponseRedirect(self.success_url)
                else:
                    messages.add_message(request, messages.ERROR, 
                                (f"{data['menu']} should have "
                                 f"{int(data['menu'].pizza.amount_toppings)} "
                                 f"toppings and food has {len(toppings)} toppings." 
                                 f"Please, check your order."))
                    return render(request,self.template_name, {"form": form, 
                                "menu": data["menu"] }) 
            # Check if food has extras and if a valid option
            extras = data_checkboxes.pop("extra",[])
            if(is_sub(data["menu"])):
                cart = Cart.objects.create(**data)
                for extra in extras:
                    extra_instance = Extra.objects.get(id=extra)
                    cart.sub_total_item += Decimal(data["quantity"])*extra_instance.price 
                    cart.extra.add(extra_instance)
                cart.save()
                messages.add_message(request, messages.INFO, 
                                    f"¡{data['menu']} added!")
                return HttpResponseRedirect(self.success_url)
            # Create item in cart
            if (not is_pizza(data["menu"]) and 
                not is_sub(data["menu"])):
                Cart.objects.create(**data)
                messages.add_message(request, messages.INFO, 
                                    f"¡{data['menu']} added!")
                return HttpResponseRedirect(self.success_url)
        return super().post(request, *args, **kwargs)    
      
class CartView(LoginRequiredMixin, ListView):
    template_name = "orders/shopping_cart.html"
    context_object_name = "carts"
    login_url = reverse_lazy("orders:login")
    STATUS_OPEN = 0  
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["total"] = Order.objects.get(Q(user=self.request.user)&
                                                Q(status=self.STATUS_OPEN)
                                                ).order_total
                                                            
        except Order.DoesNotExist:
            pass
        return context
    
    def get_queryset(self):
        return Cart.objects.filter(Q(user=self.request.user)&
                    Q(status=self.STATUS_OPEN)).prefetch_related(
                        "menu", "order")

class UpdateItemCartView(LoginRequiredMixin, UpdateView):
    template_name = "orders/form.html"
    login_url = reverse_lazy("orders:login")
    STATUS_OPEN = 0
        
    def get_queryset(self):
        return Cart.objects.filter(
            Q(user=self.request.user)&Q(status=self.STATUS_OPEN))
    
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        cart = Cart.objects.get(id=self.kwargs.get("pk",0))
        context["menu"] = cart.menu
        context["title"] = "Update Item to Cart"
        return context

    def get_form_class(self):
        cart = get_object_or_404(Cart,pk=self.kwargs.get("pk",0))
        food = cart.menu
        if (is_pizza(food)):
            if food.pizza.amount_toppings==0:
                return PizzaForm
            return PizzaToppingsForm
        if (is_sub(food)):
            return SubForm
        return CartForm

    def form_valid(self, form):
        form.instance.sub_total_item=Decimal(form.instance.quantity)*Decimal(form.instance.menu.price)
        if(is_sub(form.instance.menu)):
            for extra in self.request.POST['extra']:
                extra_qs = get_object_or_404(Extra, id=extra) 
                form.instance.sub_total_item +=Decimal(form.instance.quantity)*Decimal(extra_qs.price)
            text = (
                    f"food price {form.instance.menu.price} "
                    f"quantity {form.instance.quantity} "
                    f"total: {form.instance.sub_total_item} " 
                )
            return super().form_valid(form)        
        return super().form_valid(form)

class DeleteItemCartView(LoginRequiredMixin, DeleteView):
    template_name = "orders/form.html"
    login_url = reverse_lazy("orders:login")
    form_class = CartForm
    success_url = reverse_lazy("orders:cart")
    
    def get_queryset(self):
        STATUS_OPEN = 0
        return Cart.objects.filter(Q(user=self.request.user)&Q(status=STATUS_OPEN))
    
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        cart = Cart.objects.get(id=self.kwargs.get("pk",0))
        context["menu"] = cart.menu
        context["title"] = "Delete Item from Cart"
        return context

    def delete(self,request, *args, **kwargs):
        food = get_object_or_404(Cart,pk=self.kwargs.get("pk",0))
        messages.add_message(request,messages.INFO, f"{food.menu} was deleted!")
        return super().delete(request, *args, **kwargs)

class OrderView(LoginRequiredMixin, ListView):
    template_name = "orders/invoices.html"
    paginate_by = 3
    
    login_url = reverse_lazy("orders:login")

    def get_queryset(self):
        STATUS_DRAFT = 0
        return Order.objects.filter(~Q(status = STATUS_DRAFT) 
                    & Q(user_id = self.request.user)).order_by("-id")

class UpdateOrderView(LoginRequiredMixin, UpdateView):
    template_name = "orders/shopping_cart.html"
    login_url = reverse_lazy("orders:login")
    model = Order
    fields = ("id",)
    http_methods = ["post"]

    def get_queryset(self):
        STATUS_DRAFT = 0
        queryset = Order.objects.filter(Q(user=self.request.user)&
                        Q(status=STATUS_DRAFT) & 
                        Q(id=self.kwargs.get("pk",0)))
        return queryset
    
    def form_valid(self, form):
        STATUS_PLACE_ORDER = 1
        ITEM_RELEASE = 1
        form.instance.status = STATUS_PLACE_ORDER 
        form.save()
        Cart.objects.filter(order=form.instance).update(status=ITEM_RELEASE)              
        return super().form_valid(form)

class DetailOrderView(DetailView):
    template_name = "orders/invoices_detail.html"
    login_url = reverse_lazy("orders:login")
    STATUS_DRAFT = 0
        
    def get_queryset(self):
        queryset = Order.objects.filter(Q(user=self.request.user)&
                        ~Q(status=self.STATUS_DRAFT) & 
                        Q(id=self.kwargs.get("pk",0)))
        return queryset
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            order = Order.objects.get(Q(user=self.request.user)&
                                    ~Q(status=self.STATUS_DRAFT) & 
                                    Q(id=self.kwargs.get("pk",0)))
        except Order.DoesNotExist:
            return context
        else:
            context["carts"]=Cart.objects.filter(Q(user=self.request.user)&
                            ~Q(status=self.STATUS_DRAFT) & 
                            Q(order=order))
            context["total"] = order.order_total
            return context
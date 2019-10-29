from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.db.models import Sum
from django.views.generic import ListView, UpdateView, CreateView
from django.views import View
from django.core.paginator import Paginator
from .models import *
from .forms import *
import json
import re
import datetime
#-------------------------------------------
#               Views
#-------------------------------------------
class MenuView(View):
    def get(self, request):
        return render(request,"orders/menu.html", menu_data())

    def menu_data():
        return {'regular_pizzas': menu_format(1,True), 'sicilian_pizzas': menu_format(2,True),
                'subs': menu_format(3,True), 'pastas': menu_format(4,False),
                'salads': menu_format(5,False), 'dinners':menu_format(6,True),
                "toppings":Topping.objects.all(), "extras": Extra.objects.all()}

    def menu_format(meal_type, flag):
        menu = []
        entire_menu = Menu.objects.filter(meal_type=meal_type).order_by("ingredient")
        for food in entire_menu:
            ingredients = Menu.objects.filter(meal_type=meal_type, ingredient = food.ingredient)
            ingredient_price = {}
            for ingredient in ingredients:
                if flag:
                    if ingredient.meal_size == 1:
                        ingredient_price["small_price"] = ingredient.price
                    if ingredient.meal_size == 2:
                        ingredient_price["large_price"] =  ingredient.price
                elif not flag and ingredient.meal_size == 3:
                    ingredient_price["price"] = ingredient.price
            if flag:
                result=dict()
                for k in ingredient_price:
                    result[k]=ingredient_price[k]
                result["ingredient"]=food.ingredient.__str__()
                result["id"]=food.ingredient.id
                result["topping"]=food.topping_flag
                result["extra"]=food.extras_flag
                result["meal"]=meal_type
                if result not in menu:
                    menu.append(result)
            else:
                menu.append({"id":food.ingredient.id, "ingredient": food.ingredient.__str__(),
                "price":ingredient_price["price"], "meal": meal_type, 'topping': food.extras_flag,
                'topping': food.topping_flag})
        return menu

class OrderFood(View):
    def get(self, request, meal, ingredient_desc):
        """Short summary.

        Parameters
        ----------
        request : type
            Description of parameter `request`.
        meal : type
            Description of parameter `meal`.
        ingredient_desc : type
            Description of parameter `ingredient_desc`.

        Returns
        -------
        type
            Description of returned object.

        """
        if not request.user.is_authenticated:
            return HttpResponse(json.dumps({"login": False}))
        menu_rows = Menu.objects.filter(meal_type=meal, ingredient=ingredient_desc)
        sizes, photos = [] , []
        for menu in menu_rows:
            sizes.append(menu.SIZE[menu.meal_size-1])
            photos.append(menu.photo.url)
        return render(request,"orders/order.html", {'sizes': sizes, 'photo': photos[0],
            'meal':Menu.MEAL_TYPE[meal-1][1], 'ingredient': Ingredient.objects.get(id=ingredient_desc).__str__(),
            'ingredient_id':ingredient_desc, 'meal_id': meal, 'toppings':Topping.objects.all(),
            'extras':Extra.objects.all(), 'topping_flg':menu_rows[0].topping_flag,
            'extra_flg': menu_rows[0].extras_flag})

    def post(self, request, meal, ingredient_desc):
        """Process form and send notification as a response to user interface.

        Parameters
        ----------
        request : request
            request information from HTTP petition.
        meal : integer
            meal type id in menu model.
        ingredient_desc : integer
            ingredient id in menu model.

        Returns
        -------
        render
            Notification regarding form.

        """
        # Validation of form
        try:
            data = self.get_data(request.POST.copy(), ingredient_desc,meal)
        except Menu.DoesNotExist:
            return inflate_message_user("Please, Select size for your order!","alert alert-danger")
        except ValueError: # Not quantity Selected
            return inflate_message_user("Please, Select quantity for your order!","alert alert-danger")
        else:
            # Process data
            added = self.add_items(data)
            return self.add_order(data) if not added[0] else added[1]

    def get_data(self, data, ingredient_desc, meal):
        menu = Menu.objects.get(ingredient=ingredient_desc,meal_type=meal,
                                    meal_size=data['size'])
        total = get_total(menu.price, int(data["quantity"]), get_extra_prices(data))
        # Prepare for order form
        data.update({"user_id": self.request.user.id, "menu_id": menu.id, "status": Order_Status.STATUS[0][0],
                     "total": total, "extras":get_extras_name(data), "topping": get_topping_name(data)})
        return data

    def add_order(self, data):
        my_order = Order_StatusForm(data)
        if my_order.is_valid():
            my_order.save()
            return inflate_message_user("Added to chart!","alert alert-primary")
        else:
            return inflate_message_user(format_error_to_message(my_order.errors),"alert alert-danger")

    def add_items(self, data):
        try:
            order = Order_Status.objects.get(menu_id=data['menu_id'], status=1)
        except Order_Status.DoesNotExist:
            return (False, "")
        try:
            order.quantity = order.quantity + int(data['quantity'])
            order.total = order.total + data['total']
            if data['extras']:
                order.extras = f"{order.extras} {data['extras']}"
            if data['topping']:
                order.topping = f"{order.topping} {data['topping']}"
            order.full_clean()
        except ValidationError as e:
            return (False, "")
        else:
            order.save()
            return (True, inflate_message_user("Added to chart!","alert alert-primary"))

class Register(CreateView):
    template_name = 'orders/register.html'
    model = User
    form_class = UserForm
    success_url = "/"

class Cart(LoginRequiredMixin, ListView):
    login_url = 'register'
    queyset = Order_Status
    template_name = "orders/shopping_cart.html"

    def get_queryset(self):
        return Order_Status.objects.filter(status = 1, user_id = self.request.user)

    def post(self,request, *args, **kwargs):
        order_open = Order_Status.objects.filter(status = 1, user_id = self.request.user)
        order_tot = Order_Status.objects.filter(status = 1, user_id = self.request.user).aggregate(Sum('total'))
        new_order = Order()
        new_order.order_total = round(order_tot['total__sum'],2)
        new_order.order_date = datetime.datetime.now()
        new_order.status=2
        new_order.user = self.request.user
        new_order.save()
        for order in order_open:
            order.status=2
            order.order_id = new_order
            order.save()
        return HttpResponseRedirect(reverse('cart'))

class EditOrder(LoginRequiredMixin, View):
    login_url = 'register'
    template_name = "orders/form.html"

    def form_valid(self, form):
        return super().form_valid(form)

    def get(self, request, order_status):
        try:
            order = Order_Status.objects.get(id = order_status)
        except Order_Status.DoesNotExist:
            return Http404("Order does not exist!")
        else:
            return render(request,"orders/form.html",{"form": Order_StatusForm(instance=order),
                          "id":order_status, "order": order})

    def post(self, request, order_status):
        order = Order_Status.objects.get(id=order_status)
        if request.POST["operation"] == "Edit":
            order.quantity = request.POST["quantity"]
            order.total = int(order.quantity) * order.menu_id.price
            order.topping = request.POST.get("topping","")
            try:
                order.full_clean()
            except ValidationError as e:
                return inflate_message_user(format_error_to_message(e),"alert alert-danger")
            else:
                order.save()
                return inflate_message_user("Added to chart!","alert alert-primary")
        elif request.POST["operation"] == "Delete":
            order.delete()
            return inflate_message_user("Successful Deletion!","alert alert-primary")
        else:
            raise Http404()

class OrderTable(LoginRequiredMixin, ListView):
    login_url = 'register'
    queyset = Order_Status
    template_name = "orders/order_table.html"

    def get_queryset(self, ):
        return Order_Status.objects.filter(order_id = self.kwargs['order'], user_id = self.request.user)

class Invoice(LoginRequiredMixin, ListView):
    login_url = 'register'
    queyset = Order
    template_name = "orders/invoices.html"
    ordering =['-id']
    paginate_by = 3

    def get_queryset(self):
        return Order.objects.filter(status = 2, user_id = self.request.user)


def food_price(request, meal, ingredient, size):
    """Short summary.

    Parameters
    ----------
    request : type
        Description of parameter `request`.
    meal : type
        Description of parameter `meal`.
    ingredient : type
        Description of parameter `ingredient`.
    size : type
        Description of parameter `size`.

    Returns
    -------
    type
        Description of returned object.

    """
    return HttpResponse(Menu.objects.get(meal_type=meal, ingredient=ingredient, meal_size=size).price)

def login_form(request):
    """Short summary.

    Parameters
    ----------
    request : type
        Description of parameter `request`.

    Returns
    -------
    type
        Description of returned object.

    """
    user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponse("User is not authenticated! Please, try again!")

def logout_form(request):
    """Short summary.

    Parameters
    ----------
    request : type
        Description of parameter `request`.

    Returns
    -------
    type
        Description of returned object.

    """
    logout(request)
    return HttpResponseRedirect(reverse("index"))


#-------------------------------------------------------------------------
# Helpers functions
#-------------------------------------------------------------------------
def get_fields_for_pattern(data, pattern, model, field):
    my_list = ""
    for key in data.keys():
        if re.search(pattern, key) is not None:
            my_list += f"{getattr(globals()[model].objects.get(id=data[key]), field)} "
    return my_list

def get_extras_name(data):
    return get_fields_for_pattern(data, "extra*",type(Extra()).__name__, "extra")

def get_topping_name(data):
    return get_fields_for_pattern(data, "topping*",type(Topping()).__name__, "topping")

def get_total(price, quantity, extras_prices=None):
    """Calculate total price for menu item selected which extras included.

    Parameters
    ----------
    price : number
        price for item selected by Client.
    quantity : Integer
        amount of items desired by client for this menu item.
    extra : List of numbers
        list of prices of extras selected by client (if any).

    Returns
    -------
    Decimal
        calculated price for the items selected.

    """
    total = 0
    try:
        for extra in extras_prices:
            total += extra
    except TypeError:
        total = 0
    else:
        total += price*quantity
        return total


def inflate_message_user(message, class_css):
    """Inflate notification bar with message to client.

    Parameters
    ----------
    message : String
        information to inflate notification template.
    class_css : String
        css class used in the notification template.

    Returns
    -------
    render_to_response
        Notification infleted to be shown to user.

    """
    return render_to_response("orders/notification.html", {'class_css': class_css,
                                                          'message': message})


def format_error_to_message(post):
    """Format errors in a proper manner to be used in a HTML file.

    Parameters
    ----------
    post : dictionary
        dictionary with errors from form.

    Returns
    -------
    type
        Text with description in human readable format.

    """
    result = ""
    for k in post.keys():
       if (k != TOKEN and k !=POST_OPERATION):
            val = post[k]
            result += str(k)+" : "+ str(val[0])+ " "
    return result

def get_extra_prices(data):
    """get cost for several extras from data for client

    Parameters
    ----------
    data : dictionary
        Contains data from client, extras should be contented in keys which start with "extra".

    Returns
    -------
    list
        prices of extras selected from Client's order.

    """
    prices = []
    for key in data.keys():
        if re.search('extra*', key) is not None:
            prices.append(Extra.objects.get(id=data[key]).price)
    return prices

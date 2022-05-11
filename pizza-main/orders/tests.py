from decimal import Decimal

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse_lazy 
from django.test import tag

from orders.models import (Extra, Topping, Pizza, 
                        Sub, Salad, Pasta, DinnerPlatter,   
                        Order, Cart)
from orders.forms import (CartForm, PizzaForm, PizzaToppingsForm, SubForm)

SMALL_SIZE = 0
LARGE_SIZE = 1
REGULAR_PIZZA = 0
SICILIAN_PIZZA = 1
STATUS_IN_CART = 0
STATUS_RELEASE = 1

class RestaurantTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username="cliente",
                                email="cliente@gmail.com", 
                                password="Demo1234")

        Extra.objects.create(extra="Cheese", price=Decimal(1.00))
        Extra.objects.create(extra="Ham", price=Decimal(1.50))
        
        Topping.objects.create(topping= "Cheese")
        Topping.objects.create(topping= "Anchovies")
        Topping.objects.create(topping= "Ham")

        Pizza.objects.create(ingredient = "Cheese", 
                            price=Decimal(10.00),
                            meal_size = SMALL_SIZE,
                            meal_type = REGULAR_PIZZA,
                            amount_toppings = 0)
        Pizza.objects.create(ingredient = "1 Topping", 
                            price=Decimal(12.00),
                            meal_size = SMALL_SIZE,
                            meal_type = REGULAR_PIZZA,
                            amount_toppings = 1)
        Pizza.objects.create(ingredient = "2 Topping", 
                            price=Decimal(14.00),
                            meal_size = SMALL_SIZE,
                            meal_type = REGULAR_PIZZA,
                            amount_toppings = 2)
        
        Pizza.objects.create(ingredient = "Cheese", 
                            price=Decimal(10.00),
                            meal_size = SMALL_SIZE,
                            meal_type = SICILIAN_PIZZA,
                            amount_toppings = 0)
        Pizza.objects.create(ingredient = "1 Topping", 
                            price=Decimal(12.00),
                            meal_size = SMALL_SIZE,
                            meal_type = SICILIAN_PIZZA,
                            amount_toppings = 1)
        Pizza.objects.create(ingredient = "2 Topping", 
                            price=Decimal(14.00),
                            meal_size = SMALL_SIZE,
                            meal_type = SICILIAN_PIZZA,
                            amount_toppings = 2)
        
        Sub.objects.create(meal_size=LARGE_SIZE,
                           ingredient = "Italian Sub",
                          price = Decimal(9.50))
        Sub.objects.create(meal_size=SMALL_SIZE,
                           ingredient = "Italian Sub",
                          price = Decimal(7.75))

        Salad.objects.create(ingredient = "Garden Salad",
                          price = Decimal(7.50))
        Salad.objects.create(ingredient = "Greek Salad",
                          price = Decimal(8.95))

        Pasta.objects.create(ingredient = "Baked Ziti w/Mozzarella",
                          price = Decimal(7.75))

        DinnerPlatter.objects.create(meal_size=SMALL_SIZE,
                           ingredient = "Antipasto",
                          price = Decimal(50.00))
        DinnerPlatter.objects.create(meal_size=LARGE_SIZE,
                           ingredient = "Meatball Parm",
                          price = Decimal(75.00))

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username="cliente",)
    
            
    def check_queryset(self, output_queryset, expected_queryset):
        for out, exp in zip(output_queryset, expected_queryset):
            self.assertEqual(out.id, exp.id)
        
    def check_food(self, food, foodForm):
        response = self.client.get(reverse_lazy("orders:addcart",
                                    kwargs={"menu":food.id}))
        self.assertTemplateUsed(response=response,
                                template_name="orders/form.html")
        self.assertIn("menu",response.context)
        self.assertEqual(int(response.context["menu"].id),food.id)
        self.assertIsInstance(response.context["form"],foodForm)
        self.assertEqual(response.context["form"].initial["quantity"], 1)     
    
    
    def check_context_queryset(self, response, key, queryset):    
        self.assertIn(key,response.context)
        self.check_queryset(response.context[key],
                            queryset)
    
    def check_post(self, response, url_direct):
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url_direct)
    
    def check_cart_last_object_price(self, food, quantity, extras=0):
        last_item = Cart.objects.all().last()
        self.assertEqual((Decimal(food.price)+Decimal(extras))*Decimal(quantity), last_item.sub_total_item)

    def create_food(self, food):
        # Prepare data
        order = Order.objects.create(order_total = 0, 
                    status= STATUS_IN_CART, user = self.user)
        return Cart.objects.create(status = STATUS_IN_CART,
                    order = order, 
                    user= self.user,menu=food, quantity=1,
                    sub_total_item=Decimal(food.price)*Decimal(1))
    
    
    def check_update_item(self, food, form, url="orders:updatecart"):    
        # Create Data
        cart = self.create_food(food)
   
        # Login platform
        login = self.client.login(username='cliente', 
                                password='Demo1234')
        
        # Select Pizza and buy
        response = self.client.get(reverse_lazy(url, kwargs={"pk":cart.id}))

        if (url == "orders:updatecart"):
            self.assertEqual(response.status_code,200)
            self.assertIn("cart", response.context.keys())
            self.assertIn("menu", response.context.keys())
            self.assertIsInstance(response.context["form"],form)
            self.assertTemplateUsed(response=response,
                                template_name="orders/form.html")
        
        
        if (url == "orders:deletecart"):
            self.assertEqual(response.status_code,200)
            self.assertIn("cart", response.context.keys())
            self.assertIn("menu", response.context.keys())
            self.assertTemplateUsed(response=response,
                                template_name="orders/form.html")
            

    def check_update_item_cart_post(self, cart, quantity, extra,*, data):
        """ test for updating item in chart"""
        # Login platform
        login = self.client.login(username='cliente', 
                                password='Demo1234')
        
        # Select Pizza and buy
        response = self.client.post(reverse_lazy("orders:updatecart", kwargs={"pk":cart.id}),
                                    data)
        new_cart = Cart.objects.get(id=cart.id) # updated item
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(new_cart.quantity,quantity)
        self.assertEqual(new_cart.sub_total_item, 
                    (Decimal(cart.menu.price)*Decimal(quantity)+ Decimal(extra)*Decimal(quantity)))
        if "topping" in data.keys():
            pass

   
        
    def test_menu(self):
        # Request
        login = self.client.login(username='cliente', password='Demo1234')
        response = self.client.get(reverse_lazy("orders:index"))
        
        # Assertion with expected values
        self.assertTemplateUsed(response=response,
                                template_name="orders/menu.html")
        
        self.check_context_queryset(response, "regular_pizzas", 
                            Pizza.objects.filter(meal_type = REGULAR_PIZZA))
        
        self.check_context_queryset(response, "sicilian_pizzas", 
                            Pizza.objects.filter(meal_type = SICILIAN_PIZZA))
        
        self.check_context_queryset(response, "subs", 
                            Sub.objects.all())
        
        self.check_context_queryset(response, "salads", 
                            Salad.objects.all())

        self.check_context_queryset(response, "pastas", 
                            Pasta.objects.all())
        
        self.check_context_queryset(response, "dinner_platters", 
                            DinnerPlatter.objects.all())

        self.check_context_queryset(response, "toppings", 
                            Topping.objects.all())

        self.check_context_queryset(response, "extras", 
                            Extra.objects.all())

    def test_get_add_item_cart(self):
        
        login = self.client.login(username='cliente', password='Demo1234')
        
        self.check_food(Pizza.objects.all().first(),PizzaForm)
        
        self.check_food(Pizza.objects.filter(amount_toppings = 1).first(),
                        PizzaToppingsForm)
        
        self.check_food(Sub.objects.all().first(),
                        SubForm)
        
        self.check_food(Salad.objects.all().first(),
                        CartForm)
        
        self.check_food(Pasta.objects.all().first(),
                        CartForm)
        
        self.check_food(DinnerPlatter.objects.all().first(),
                        CartForm)
    
    def test_post_add_item_cart(self):
        # Login platform
        login = self.client.login(username='cliente', 
                                password='Demo1234')
        opened_order = Order.objects.filter(user=self.user,
                                            status = STATUS_IN_CART)
        if not opened_order.exists():
            print("\nInitially should not be open orders")
        # Select Pizza and buy
        food = Pizza.objects.all().first()
        response = self.client.post(reverse_lazy("orders:addcart", kwargs={"menu":food.id}),
                                    {"quantity":1})
        self.check_post(response, reverse_lazy("orders:cart"))
        self.check_cart_last_object_price(food, 1)
        new_order = Order.objects.filter(user=self.user,
                                            status = STATUS_IN_CART)
        self.assertTrue(new_order.exists())
        cart_last_item = Cart.objects.filter(user=self.user,status = STATUS_IN_CART).last()
        self.assertEqual(cart_last_item.order.id,new_order.last().id)
        
        # Select Pizza with topping and buy
        food = Pizza.objects.filter(amount_toppings = 1).first()
        topping = Topping.objects.all().first()
        response = self.client.post(reverse_lazy("orders:addcart", 
                                    kwargs={"menu":food.id }),
                                    {"quantity":1, "toppings": [f"{topping.id}",]})
        self.check_post(response, reverse_lazy("orders:cart"))
        self.check_cart_last_object_price(food, 1)
        order_again = Order.objects.filter(user=self.user,
                                            status = STATUS_IN_CART)
        # Not create new orders
        self.assertEqual(new_order.last().id, order_again.last().id)
        cart_last_item = Cart.objects.filter(user=self.user,status = STATUS_IN_CART).last()
        self.assertEqual(cart_last_item.order.id,new_order.last().id) # Check order is added to existant order
        

        # Select Sub with extra and buy
        food = Sub.objects.all().first()
        extra = Extra.objects.all().first()
        response = self.client.post(reverse_lazy("orders:addcart", 
                                    kwargs={"menu":food.id}),
                                    {"quantity":2, "extra": [f"{extra.id}",]})
        self.check_post(response, reverse_lazy("orders:cart"))
        self.check_cart_last_object_price(food, 2, extra.price)
        
        # Select Sub w/o extra and buy
        response = self.client.post(reverse_lazy("orders:addcart", 
                                    kwargs={"menu":food.id}),
                                    {"quantity":1})
        self.check_post(response, reverse_lazy("orders:cart"))
        self.check_cart_last_object_price(food, 1)
        
        # Select Salad with extra and buy
        food = Salad.objects.all().first()
        response = self.client.post(reverse_lazy("orders:addcart", 
                                    kwargs={"menu":food.id,}),
                                    {"quantity":1})
        self.check_post(response, reverse_lazy("orders:cart"))
        self.check_cart_last_object_price(food, 1)
        
        # Select Pasta with extra and buy
        food = Pasta.objects.all().first()
        response = self.client.post(reverse_lazy("orders:addcart", 
                                    kwargs={"menu":food.id,}),
                                    {"quantity":1})
        self.check_post(response, reverse_lazy("orders:cart"))
        self.check_cart_last_object_price(food, 1)
        
        # Select Dinner Platter with extra and buy
        food = DinnerPlatter.objects.all().first()
        response = self.client.post(reverse_lazy("orders:addcart", 
                                    kwargs={"menu":food.id,}),
                                    {"quantity":1})
        self.check_post(response, reverse_lazy("orders:cart"))
        self.check_cart_last_object_price(food, 1)
        

    def test_post_bad_add_item_cart(self):
        # Login platform
        login = self.client.login(username='cliente', 
                                password='Demo1234')
        # Select Pizza and buy
        food = Pizza.objects.all().first()
        response = self.client.post(reverse_lazy("orders:addcart", kwargs={"menu":food.id}),
                                    {"quantity":-1})
        self.assertEqual(response.status_code,200)
        self.assertIn( "quantity",response.context["form"].errors.keys())

        # Select Pizza with topping and buy
        food = Pizza.objects.filter(amount_toppings = 1).first()
        topping = Topping.objects.all()
        response = self.client.post(reverse_lazy("orders:addcart", 
                                    kwargs={"menu":food.id }),
                                    {"quantity":1, "toppings": [f"{topping[0].id}",f"{topping[1].id}"]})
        self.assertEqual(response.status_code,200)
        self.assertNotEqual(response.context["messages"],[]) 
    
    @tag("cart")
    def test_get_cart(self):
        login = self.client.login(username='cliente', 
                                password='Demo1234')
        response = self.client.get(reverse_lazy("orders:cart"))
        self.assertIn("total", response.context)
        self.assertIn("carts", response.context)
        
    @tag("cart")
    def test_check_place_order_features(self):
        # Prepare data
        food = Pizza.objects.all().first()            
        order = Order.objects.create(order_total = 0, 
                    status= STATUS_IN_CART, user = self.user)
        cart = Cart.objects.create(status = STATUS_IN_CART,
                    order = order, 
                    user= self.user,menu=food, quantity=1,
                    sub_total_item=Decimal(food.price)*Decimal(1))
        # POST data
        login = self.client.login(username='cliente', 
                    password='Demo1234')
        response = self.client.post(reverse_lazy("orders:updateinvoices",
                        kwargs={"pk":cart.order.id}))
        # Assert response
        self.check_post(response, reverse_lazy("orders:invoices"))
        new_cart = Cart.objects.get(id=cart.id)
        self.assertEqual(new_cart.status, STATUS_RELEASE)

    @tag("cart")
    def test_check_get_place_order_features(self):
        """ it should not allowed get method"""
        # Prepare data
        food = Pizza.objects.all().first()            
        cart = self.create_food(food)
        # POST data
        login = self.client.login(username='cliente', 
                    password='Demo1234')
        response = self.client.get(reverse_lazy("orders:updateinvoices",
                        kwargs={"pk":cart.order.id}))
        # Assert response
        print(response.status_code)

    @tag("update_cart")
    def test_update_item_cart_pizza_no_topping_get(self):
        """ test for getting item in chart for update"""
        # Create Data
        food = Pizza.objects.all().first()            
        self.check_update_item(food, PizzaForm)
        
    @tag("update_cart")
    def test_update_item_cart_pizza_no_topping_post(self):
        """ test for updating item in chart"""
        # Create Data
        food = Pizza.objects.all().first()            
        cart = self.create_food(food)
        self.check_update_item_cart_post(cart,2,0, data={"quantity":2})

    @tag("update_cart")
    def test_update_item_cart_pizza_topping_get(self):
        """ test for getting item in chart for update"""
        # Create Data
        food = Pizza.objects.filter(amount_toppings=1).first()            
        self.check_update_item(food, PizzaToppingsForm)
        
    @tag("update_cart")
    def test_update_item_cart_pizza_topping_post(self):
        """ test for updating item in chart"""
        # Create Data
        food = Pizza.objects.filter(amount_toppings=1).first()            
        cart = self.create_food(food)
        top = Topping.objects.all()
        cart.toppings.add(top[0])
        self.check_update_item_cart_post(cart,2,0,data={"quantity":2})

        self.check_update_item_cart_post(cart,2,0, 
                        data={"quantity":2, "toppings": [f"{top[1].id}"],})

    @tag("update_cart")
    def test_update_item_cart_sub_extra_get(self):
        """ test for getting item in chart for update"""
        # Create Data
        food = Sub.objects.all().first()            
        self.check_update_item(food, SubForm)
        
    @tag("update_cart", "update_sub")
    def test_update_item_cart_sub_extra_post(self):
        """ test for updating item in chart"""
        # Create Data
        food = Sub.objects.all().first()            
        cart = self.create_food(food)
        extra = Extra.objects.all()
        cart.extra.add(extra[0])
        self.check_update_item_cart_post(cart,2,extra[0].price,data={"quantity":2})
        
    @tag("update_cart", "update_sub", "update_sub_extra")
    def test_update_item_cart_sub_extra_post(self):
        """ test for updating item in chart"""
        # Create Data
        food = Sub.objects.all().first()            
        cart = self.create_food(food)
        extra = Extra.objects.all()
        cart.extra.add(extra[0])
        self.check_update_item_cart_post(cart,2,extra[1].price, 
                         data={"quantity":2, "extra": [f"{extra[1].id}"],})


    @tag("update_cart")
    def test_update_item_cart_salad_extra_get(self):
        """ test for getting item in chart for update"""
        # Create Data
        food = Salad.objects.all().first()            
        self.check_update_item(food, CartForm)
        
    @tag("update_cart")
    def test_update_item_cart_salad_extra_post(self):
        """ test for updating item in chart"""
        # Create Data
        food = Salad.objects.all().first()            
        cart = self.create_food(food)
        self.check_update_item_cart_post(cart,2,0,data={"quantity":2})

    @tag("update_cart")
    def test_update_item_cart_pasta_extra_get(self):
        """ test for getting item in chart for update"""
        # Create Data
        food = Pasta.objects.all().first()            
        self.check_update_item(food, CartForm)
        
    @tag("update_cart")
    def test_update_item_cart_pasta_extra_post(self):
        """ test for updating item in chart"""
        # Create Data
        food = Pasta.objects.all().first()            
        cart = self.create_food(food)
        self.check_update_item_cart_post(cart,2,0,data={"quantity":2})

    @tag("update_cart")
    def test_update_item_cart_dinner_extra_get(self):
        """ test for getting item in chart for update"""
        # Create Data
        food = DinnerPlatter.objects.all().first()            
        self.check_update_item(food, CartForm)
        
    @tag("update_cart")
    def test_update_item_cart_dinner_extra_post(self):
        """ test for updating item in chart"""
        # Create Data
        food = DinnerPlatter.objects.all().first()            
        cart = self.create_food(food)
        self.check_update_item_cart_post(cart,2,0,data={"quantity":2})

    @tag("delete_cart")
    def test_delete_item_cart_dinner_extra_get(self):
        """ test for getting item in chart for update"""
        # Create Data
        food = DinnerPlatter.objects.all().first()            
        self.check_update_item(food, CartForm, "orders:deletecart")
        
    @tag("delete_cart")
    def test_delete_item_cart_dinner_extra_post(self):
        """ test for updating item in chart"""
        # Create Data
        food = DinnerPlatter.objects.all().first()            
        cart = self.create_food(food)
        
        # Delete
        login = self.client.login(username='cliente', 
                    password='Demo1234')
        response = self.client.post(reverse_lazy("orders:deletecart", 
                                    kwargs={"pk":cart.id }))
        
        # Assert values
        self.check_post(response, reverse_lazy("orders:cart"))

    def test_order_view(self):
        # Create item 
        food = DinnerPlatter.objects.all().first()            
        cart = self.create_food(food)
        cart.status = STATUS_RELEASE
        cart.save()

        # Request
        login = self.client.login(username='cliente', 
                    password='Demo1234')
        response = self.client.get(reverse_lazy("orders:invoices"))
        
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIn("order_list", response.context.keys())

    def test_order_detail(self):
        # Create item 
        food = DinnerPlatter.objects.all().first()            
        cart = self.create_food(food)
        cart.status = STATUS_RELEASE
        cart.save()
        order = cart.order
        order.status = STATUS_RELEASE
        order.save()

        # Request
        login = self.client.login(username='cliente', 
                    password='Demo1234')
        response = self.client.get(reverse_lazy("orders:detailinvoices", 
                        kwargs={"pk": order.id}))
        
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIn("object", response.context.keys())
        self.assertIn("carts", response.context.keys())
        self.assertIn("editable", response.context.keys())
        self.assertIn("total", response.context.keys())

    def test_signal_add_cart(self):
        food = Pizza.objects.filter(amount_toppings=1).first()            
        cart = self.create_food(food)
        quantity = 1
        total = Decimal(food.price)*Decimal(quantity)
        order = Order.objects.get(id=cart.order.id)
        self.assertEqual(order.order_total,total)
        
        food = Sub.objects.all().first()            
        Cart.objects.create(status = STATUS_IN_CART,
                    order = order, 
                    user= self.user,menu=food, quantity=1,
                    sub_total_item=Decimal(food.price)*Decimal(1))
        total += Decimal(food.price)*Decimal(quantity)
        order = Order.objects.get(id=cart.order.id)
        self.assertEqual(order.order_total,total)
        
    def test_signal_remove_cart(self):
        # Create item in cart
        first_item = Pizza.objects.filter(amount_toppings=1).first()            
        cart = self.create_food(first_item)
        
        # Totalize total order
        quantity = 1
        total = Decimal(first_item.price)*Decimal(quantity)
        order = Order.objects.get(id=cart.order.id)
        
        #Create other item in cart
        second_item = Sub.objects.all().first()            
        Cart.objects.create(status = STATUS_IN_CART,
                    order = order, 
                    user= self.user,menu=second_item, quantity=1,
                    sub_total_item=Decimal(second_item.price)*Decimal(1))
        # Totalize entire order
        total += Decimal(second_item.price)*Decimal(quantity)
        
        # Delete first item of cart
        Cart.objects.get(id=cart.id).delete()
        # Totalize
        total -= Decimal(first_item.price)*Decimal(quantity)
        
        # Get Order
        order = Order.objects.get(id=cart.order.id)
        # Total should be the entire total without the first item
        self.assertEqual(order.order_total,total)
        
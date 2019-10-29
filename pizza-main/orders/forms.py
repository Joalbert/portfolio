from .models import *
from django.forms import ModelForm, Form
from django import forms
from django.contrib.auth.forms import UserCreationForm


class IngredientForm(ModelForm):
    class Meta:
        """docstring for Meta"""
        model = Ingredient
        fields = "__all__"


class ExtraForm(ModelForm):
    class Meta:
        """docstring for Meta"""
        model = Extra
        fields = "__all__"


class ToppingForm(ModelForm):
    class Meta:
        """docstring for Meta"""
        model = Topping
        fields = "__all__"


class OrderForm(ModelForm):
    class Meta:
        """docstring for Meta"""
        model = Order
        fields = "__all__"


class MenuForm(ModelForm):
    class Meta:
        """docstring for Meta"""
        model = Menu
        fields = "__all__"


class AddChartForm(Form):
    quantity = forms.IntegerField(min_value=0)
    size = forms.ChoiceField(choices=Menu.SIZE)
    

class Order_StatusForm(ModelForm):
    class Meta:
        """docstring for Meta"""
        model = Order_Status
        fields = "__all__"


class UserForm(UserCreationForm):
    username = forms.CharField(label = "User", max_length=30, required=True, help_text = None)
    last_name = forms.CharField(label = "Last Name", max_length=30, required=False, help_text = None)
    first_name = forms.CharField(label = "Name", max_length=30, required=False, help_text = None)
    email = forms.EmailField(label = "Email", max_length=254, required= True, help_text = None)
    password1 = forms.CharField(label="Password", help_text = None, widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password", help_text = "Retype password",widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

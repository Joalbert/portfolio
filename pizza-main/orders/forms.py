from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from orders.models import Cart, Topping


class CartForm(forms.ModelForm):
    class Meta:
        """docstring for Meta"""
        model = Cart
        fields = ["quantity"]


class PizzaForm(forms.ModelForm):
    class Meta:
        """docstring for Meta"""
        model = Cart
        fields = ["quantity"]


class PizzaToppingsForm(forms.ModelForm):
    
    class Meta:
        """docstring for Meta"""
        model = Cart
        fields = ["quantity","toppings"]
        widgets = {
            'toppings' : forms.CheckboxSelectMultiple(),   
        }


class SubForm(forms.ModelForm):
    class Meta:
        """docstring for Meta"""
        model = Cart
        fields = ["quantity","extra"]
        widgets = {
            'extra' : forms.CheckboxSelectMultiple(),   
        }

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

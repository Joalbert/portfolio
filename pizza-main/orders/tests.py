from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import *
from .. import populate_data
# Create your tests here.

class RestaurantTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        populate_data.run()

    def test_food_form_ok():
        data = {"size":1,"quantity":1,"extra_1":1}
        food_form(data, Menu.MEAL_TYPE[2], 7)

    def test_get_extra_prices(data):
        data = {"additional":"extra_1", "quantity": 3, "size":1, }
        self.assertTrue()

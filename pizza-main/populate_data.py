from orders.models import *
from django.contrib.auth.models import User
import csv
def run():
    ''' Load default data in database to use web application.

    Return:
        None
    '''
    if not User.objects.filter(username="pizza_admin").exists():
        pizza_user = User.objects.create_superuser(username="pizza_admin",
                    email="pizza_admin@example.com", password="P1zza4dmin!")
    if not Topping.objects.all().exists():
        load_data("initial_data/Toppings.csv","Topping",("topping",))
    if not Ingredient.objects.all().exists():
        load_data("initial_data/Ingredient.csv","Ingredient",("ingredient",))
    if not Extra.objects.all().exists():
        load_data("initial_data/Extra.csv","Extra",("extra","price"))


def load_data(file_location, model_name, model_fields):
    '''
    Read csv file and load information into model

    Args:
        file_location: indicate where is the file
        model_name: indicate model name, it should be a valid model in orders.model
        model_fields: is a tuple with fields from the model_name, the data should be
            ordered in the same order as the fields are indicated at the function

    Returns:
        None
    '''
    with open(file_location) as f:
        reader = csv.reader(line,delimiter=" ")
        line_count = 0
        for row in reader:
            for i, field in enumerate(model_fields):
                datum[field]=row[i]
            my_model = globals()[model_name](**datum)
            my_model.save()

if __name__ == '__main__':
    run()

import re
from django.shortcuts import render_to_response
from orders.models import (Extra, Topping) 
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

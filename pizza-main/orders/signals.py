from decimal import Decimal

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.db.models import Sum

from orders.models import Cart, Order
from orders.helpers import is_sub

@receiver(post_save, sender=Cart)
def listen_post_save_cart(sender, instance, **kwargs):
    try:
        total = Cart.objects.filter(order=instance.order).aggregate(Sum("sub_total_item"))
        instance.order.order_total = total["sub_total_item__sum"]  
        instance.order.save()
    except Order.DoesNotExist:
        print("Order was not created previously, There is a bug!!")
        raise

@receiver(pre_delete, sender=Cart)
def listen_post_delete_cart(sender, instance, **kwargs):
    try:
        order = Order.objects.get(id=instance.order.id)
        order.order_total -= instance.sub_total_item
        order.save()
    except Order.DoesNotExist:
        instance.order.order_total
        raise
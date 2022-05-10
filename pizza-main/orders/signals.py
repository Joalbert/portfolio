from decimal import Decimal

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db.models import Sum

from orders.models import Cart, Sub
from orders.helpers import is_sub

@receiver(post_save, sender=Cart)
def listen_post_save_cart(sender, instance, **kwargs):
    total = Cart.objects.filter(order=instance.order).aggregate(Sum("sub_total_item"))
    instance.order.order_total = total["sub_total_item__sum"]
    instance.order.save()

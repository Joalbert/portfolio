# Generated by Django 3.2.12 on 2022-05-09 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0030_alter_cart_extra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='extra',
            field=models.ManyToManyField(blank=True, related_name='CartExtra', to='orders.Extra'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Open'), (1, 'Release')], default=0),
        ),
        migrations.AlterField(
            model_name='cart',
            name='toppings',
            field=models.ManyToManyField(blank=True, related_name='CartTopping', to='orders.Topping'),
        ),
    ]

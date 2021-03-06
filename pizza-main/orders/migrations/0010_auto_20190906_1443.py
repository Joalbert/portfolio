# Generated by Django 2.2.4 on 2019-09-06 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_auto_20190222_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extra',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='menu',
            name='meal_size',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Small'), (2, 'Large'), (3, 'Standard')]),
        ),
        migrations.AlterField(
            model_name='menu',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='order_status',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.DeleteModel(
            name='Size',
        ),
    ]

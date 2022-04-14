# Generated by Django 2.2.4 on 2019-09-06 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_auto_20190906_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='meal_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Regular Pizza'), (2, 'Sicilian Pizza'), (3, 'Sub'), (4, 'Pasta'), (5, 'Salad'), (6, 'Dinner Platter')]),
        ),
        migrations.DeleteModel(
            name='Meal',
        ),
    ]

# Generated by Django 2.0.3 on 2019-02-22 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20190221_1336'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order_status',
            name='Quantity',
        ),
        migrations.RemoveField(
            model_name='order_status',
            name='status_id',
        ),
        migrations.AddField(
            model_name='order',
            name='order_total',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='order_status',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='order_status',
            name='status',
            field=models.CharField(default='Open', max_length=4),
        ),
        migrations.AlterField(
            model_name='order_status',
            name='total',
            field=models.FloatField(default=0),
        ),
    ]

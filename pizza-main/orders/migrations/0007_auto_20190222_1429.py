# Generated by Django 2.0.3 on 2019-02-22 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20190222_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_status',
            name='order_id',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='Order', to='orders.Order'),
        ),
    ]

# Generated by Django 2.2.4 on 2019-10-27 22:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0012_auto_20190906_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Open'), (2, 'Done')], default=1),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='OrderUser', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='order_status',
            name='extras',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='order_status',
            name='topping',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]

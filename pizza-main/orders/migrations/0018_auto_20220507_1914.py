# Generated by Django 3.2.13 on 2022-05-07 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0017_auto_20220507_1910'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chart',
            old_name='menu_id',
            new_name='menu',
        ),
        migrations.RenameField(
            model_name='chart',
            old_name='order_id',
            new_name='order',
        ),
        migrations.RenameField(
            model_name='chart',
            old_name='user_id',
            new_name='user',
        ),
    ]

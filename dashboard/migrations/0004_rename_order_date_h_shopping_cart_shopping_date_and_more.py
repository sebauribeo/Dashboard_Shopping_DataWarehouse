# Generated by Django 4.1.4 on 2024-05-11 22:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_rename_customer_id_h_shopping_cart_customer_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='h_shopping_cart',
            old_name='order_date',
            new_name='shopping_date',
        ),
        migrations.RemoveField(
            model_name='h_shopping_cart',
            name='age',
        ),
        migrations.RemoveField(
            model_name='h_shopping_cart',
            name='city',
        ),
        migrations.RemoveField(
            model_name='h_shopping_cart',
            name='customer_name',
        ),
        migrations.RemoveField(
            model_name='h_shopping_cart',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='h_shopping_cart',
            name='home_address',
        ),
    ]
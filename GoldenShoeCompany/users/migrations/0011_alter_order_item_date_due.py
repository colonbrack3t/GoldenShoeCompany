# Generated by Django 4.0.4 on 2022-05-30 20:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_order_item_date_due'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_item',
            name='date_due',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]

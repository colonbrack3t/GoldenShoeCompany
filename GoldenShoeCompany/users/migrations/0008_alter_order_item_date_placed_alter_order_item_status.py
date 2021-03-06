# Generated by Django 4.0.4 on 2022-05-30 15:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_order_item_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_item',
            name='date_placed',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='order_item',
            name='status',
            field=models.CharField(default='Processing', max_length=32, null=True),
        ),
    ]

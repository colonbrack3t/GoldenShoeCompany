# Generated by Django 4.0.4 on 2022-05-27 22:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('users', '0003_basket_item_user_alter_basket_item_item_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket_item',
            name='image',
            field=models.ForeignKey(default=None, null = True, on_delete=django.db.models.deletion.CASCADE, to='products.shoe_image'),
            preserve_default=False,
        ),
    ]

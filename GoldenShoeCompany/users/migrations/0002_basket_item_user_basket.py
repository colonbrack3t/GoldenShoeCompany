# Generated by Django 4.0.4 on 2022-05-27 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='basket_item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.shoe_stock')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='basket',
            field=models.ManyToManyField(related_name='basket_items', null=True, to='users.basket_item'),
        ),
    ]

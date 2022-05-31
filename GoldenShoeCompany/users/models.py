from asyncio import BaseEventLoop
from django.db import models
import random
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
class User(AbstractUser):
    api_key = models.CharField(max_length=64)

    def create_api_key(self):
        def generate_unique_order_number():
            while True:
                n = '%030x' % random.randrange(16**64)
                if len(User.objects.filter(api_key=n))==0:
                    return n
        self.api_key = generate_unique_order_number()
        self.save()
class Basket_Item(models.Model):
    item = models.ForeignKey('products.shoe_stock', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    user = models.ForeignKey('user',null=True,on_delete=models.CASCADE)
    image = models.ForeignKey('products.shoe_image', on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        if self.quantity<=0:
            self.delete()
        else:
            super(Basket_Item, self).save(*args, **kwargs)
class OrderManager(models.Manager):
        def create_order_remove_basket(self, basket_item, delivery_timedelta):
            def generate_unique_order_number():
                while True:
                    n = '%030x' % random.randrange(16**30)
                    if len(Order_Item.objects.filter(order_number=n))==0:
                        return n

            order = self.create(user = basket_item.user, 
                               image = basket_item.image , 
                               quantity = basket_item.quantity,
                               order_number = generate_unique_order_number(),
                               item = basket_item.item)
            order.date_due = order.date_placed + delivery_timedelta 
            order.save()
            basket_item.delete()
            return order
class Order_Item(models.Model):
    user = models.ForeignKey('user',null=True,on_delete=models.CASCADE)
    date_placed = models.DateTimeField(default = timezone.now)
    date_due = models.DateField(default = timezone.now)
    image = models.ForeignKey('products.shoe_image', on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    order_number = models.CharField(max_length=32)
    item = models.ForeignKey('products.shoe_stock', on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=32, null=True, default="Processing")
    objects = OrderManager()
    def total_price(self):
        return self.quantity * self.item.product.price
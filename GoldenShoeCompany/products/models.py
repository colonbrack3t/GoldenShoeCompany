from django.db import models
from django.forms import IntegerField
from multiselectfield import MultiSelectField
# Create your models here.
class product(models.Model):
    product_name  = models.CharField(max_length=128)
    description  = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField()
class shoe(product):
    size = IntegerField()
    category_choices = (
        (1 , "Casual"),
        (2 , "Sport") 
        )
    gender = models.CharField(max_length=6, choices= (("M", "MEN"), ("W","WOMEN")))
    category = MultiSelectField(choices=category_choices)
    
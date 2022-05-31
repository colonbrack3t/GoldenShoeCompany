from distutils.command.upload import upload
from django.db import models
from multiselectfield import MultiSelectField
from colorfield.fields import ColorField
from django.conf import settings
from PIL import Image


#generic product database record
class product(models.Model):
    #these should be seperate category and product models 
    category_choices = settings.SHOE_CATEGORIES
   
    name               = models.CharField(max_length=128)
    description        = models.TextField()
    short_description  = models.TextField()
    price              = models.DecimalField(max_digits=6, decimal_places=2)
    gender             = models.CharField(max_length=6, choices= (("M", "MEN"), ("W","WOMEN")))
    category           = MultiSelectField(choices=category_choices)
    
    def __str__(self):
        return self.name
    # gets total stock of all sizes and colors
    def get_stock(self):
        stock = 0
        for s in shoe_stock.objects.filter(product=self):
            stock+=s.stock
        return stock
# stock for specific shoe (with size and color)
class shoe_stock (models.Model):
    product = models.ForeignKey('product', on_delete=models.PROTECT)
    stock   = models.IntegerField()
    size    = models.IntegerField()
    color = models.ForeignKey('shoe_color', on_delete=models.PROTECT, null=True)
    def __str__(self):
        return self.product.name
#shoe image record
class shoe_image(models.Model):
    image = models.ImageField(upload_to='products/png/shoes')
    shoe  = models.ForeignKey('product', on_delete=models.PROTECT)
    is_primary = models.BooleanField(null=True)

#color record
class shoe_color(models.Model):
    color_name       = models.CharField(max_length=128)
    hex_color            = ColorField(format="hex")
    def __str__(self):
        return self.color_name
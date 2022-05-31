from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)
class ShoeStockAdmin(admin.ModelAdmin):
    list_display = ('product','color','size')
class ImageAdmin(admin.ModelAdmin):
    list_display = ('shoe','is_primary')
class ColorPickerAdmin(admin.ModelAdmin):
    list_display = ('color_name', 'color', )                         
                                                                                                                             
                                                                                                                             
    def color(self, obj):
        h = obj.hex_color.lstrip('#')
        inverted_rgb = tuple((255 - int(h[i:i+2], 16)) for i in (0, 2, 4))
        inverted_hex = '#%02x%02x%02x' % inverted_rgb
        return mark_safe(u'<div style="padding: 3px; background:{}; color : {}"><b>{}</b></div>'.format(obj.hex_color, inverted_hex, obj.hex_color) )                                               
   
admin.site.register(shoe_stock,ShoeStockAdmin)
admin.site.register(product, ProductAdmin)
admin.site.register(shoe_image,ImageAdmin)
admin.site.register(shoe_color, ColorPickerAdmin)

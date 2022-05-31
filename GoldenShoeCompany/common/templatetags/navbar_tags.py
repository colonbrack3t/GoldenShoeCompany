from django import template
from users.models import Basket_Item
register = template.Library()

@register.filter
def basket_items_count(user):
    return len(Basket_Item.objects.filter(user=user))
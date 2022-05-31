import re
from django.shortcuts import render
from django.conf import settings 
from products.models import *
#front page view
def main_page(request):
    sport_items = divide_into_n(list(shoe_image.objects.all())*4,3)
    return render(request,  'html/main_page.html', {"sport_items" : sport_items})


#page view for men's products
def men_page(request):
    get = {}
    if request.GET:
        get = dict(request.GET)
    return render(request, 'html/product_page.html', {"gender" : "M", "categories" : settings.SHOE_CATEGORIES, "filter" : get})
#divides list l into a list of lists of size n
#eg divide_into_n(range(6),3) => [ [0 , 1 , 2] , [3 , 4 , 5] ]
def divide_into_n(l, n):
   output = []           
   for i in range(0,len(l),n):
     set = []
     for m in range(n):
        if i+m<len(l):
            set.append(l[i+m])
     output.append(set)
   return output
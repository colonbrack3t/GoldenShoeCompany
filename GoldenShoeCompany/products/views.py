from django.shortcuts import render, redirect
from django.http import JsonResponse
from users.models import Basket_Item
from .models import *

# called when the products page is polling for more products to show
def fetch_products(request):
    data = dict(request.POST.items())
    # index and size of request, to only get a slice of db
    data['index'] = int(data['index'])
    data['size'] = int(data['size'])
    # filter db by gender, and consistent order
    products_models = product.objects.all().filter(gender = data.get('gender')).order_by('pk')
    
    # filter products more if user has selected category filters
    if 'filters' in data and data['filters']!='':
        #parse filters 
        filters = data['filters'].replace('["',"").replace('"]',"").split('", "')
        # create empty query set - accumulator
        products_models_filtered = product.objects.none()
        
        for category in filters:
            category_id = category.split(", ")[0][1:]
            products_models_temp=products_models.filter(category=category_id)
            # append products that match filter to accumulator
            products_models_filtered=products_models_filtered | products_models_temp
        # set output product models as accumulator
        products_models = products_models_filtered
    # remove any out of stock items
    products_models=[p for p in list(products_models) if p.get_stock()>0]
    # take slice of products
    products = products_models[data['index']:data['index']+data['size']]
    #create html code for each product
    res = {"products" : []}
    for item in products:
        
        img = get_primary_image(item)
        content = render(request, 'html/shoe_product_card.html', {'item' : item, 'image_model' : img}).content.decode()
        json_str = str(content).replace('"',"'")
        res["products"].append(json_str)

    #return collection of html codes    
    return JsonResponse(res)
#gets primary image of a shoe_stock. If none, then it selects the first image
def get_primary_image(item):
    images = shoe_image.objects.filter(shoe=item).order_by('pk')
    img = None
    try:
        img = images.filter(is_primary = True)[0]
    except:
        img = images[0]
    return img
        
#view for a product's individual page
def single_product_page(request, id):
    # Post request when user has selected to add item to basket
    if request.POST:
        if not request.user.is_authenticated:
            return redirect('sign_up')
        post = dict(request.POST.items())
        if "ColorAndSize" in post:
            #get all relevant db records
            p = product.objects.filter(id=post['product']).first()
            color_name , size = post["ColorAndSize"].split(":")
            color = shoe_color.objects.filter(color_name = color_name).first()
            

            stock_item = shoe_stock.objects.filter(product=p).filter(size = size).filter(color = color).first()
            existing_basket_item = Basket_Item.objects.filter(user = request.user).filter(item = stock_item)
            result = {'new_item':True}
            # if item is already in basket only increment quantity by 1 instead of adding a new item
            if len(existing_basket_item) > 0:
                basket_item = existing_basket_item.first()
                basket_item.quantity += 1
                basket_item.save()
                result = {'new_item':False}
            else:
                img = get_primary_image(stock_item.product)
                basket_item = Basket_Item(item = stock_item, quantity = 1, user=request.user, image=img)
                basket_item.save()
            return JsonResponse(result)
    # get all data of this product
    item = product.objects.filter(id = id)[0]
    images = shoe_image.objects.filter(shoe=item)
    stock_db = shoe_stock.objects.filter(product=item).filter(stock__gt=0).order_by('size')
    stocks_by_size = {}
    # create dictionary of format { size_value : [(color_record of stock of this size_value , stock number of this item with this color_record and size_value), .. ]}
    for stock in stock_db:
       if stock.size  in stocks_by_size:
           stocks_by_size[stock.size].append((stock.color, stock.stock))

       else:
           stocks_by_size[stock.size] = [(stock.color, stock.stock),]
    return render(request, 'html/single_product_page.html', {'item' : item, "images" : images, "stocks":stocks_by_size})
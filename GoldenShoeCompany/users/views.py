from tkinter import N
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as login_auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import prefetch_related_objects
from django.shortcuts import redirect
from datetime import timedelta
from .models import Basket_Item, Order_Item
from .forms import *

# sign up and login boilerplate code
def sign_up(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login_auth(request, user)
            # redirect
    else: 
        form = SignupForm()
    return render(request, 'html/signup.html',{'form' : form})



def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login_auth(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.error(request,"Invalid username or password.")
                
        else:
            messages.error(request,"Invalid username or password.")
            
    form = AuthenticationForm()
    return render(request=request, template_name="html/login.html", context={"login_form":form})

def log_out(request):
    logout(request)
    return redirect('/')

# gets total price of a basket
def get_basket_total(basket):
    output = 0
    for item in basket:
        output += (item.item.product.price * item.quantity)
    return output
#basket page view
def basket(request):
    if not request.user.is_authenticated:
        return redirect('sign_up')
    
    basket = Basket_Item.objects.filter(user = request.user).order_by('pk')
    if len(basket)==0:
        return render(request, 'html/emptybasket.html')
    prefetch_related_objects(basket,'item')
    prefetch_related_objects(basket,'image')
    
    return render(request, 'html/basket.html',{'basket' : basket, 'total' : get_basket_total(basket)})
#checkout page view
def checkout(request):
    if not request.user.is_authenticated:
        return redirect('sign_up')
    basket = Basket_Item.objects.filter(user = request.user)
    #if user has selected to pay, we now delete the basket items, update stock and redirect user to front page
    if request.POST:
        delivery_option = dict(request.POST.items())['delivery']
        delivery_timedelta = timedelta(days=5 if delivery_option == 0 else 1)
        
        for item in basket:
           
            
            out_of_stock = False
            if item.item.stock <= item.quantity:
                out_of_stock=True
     

            else:
                stock_item = item.item
                stock_item.stock -= item.quantity
                stock_item.save()
            order_item = Order_Item.objects.create_order_remove_basket(item, delivery_timedelta)
            if out_of_stock:
                order_item.status = "Cancelled, out of stock!"
                
        return redirect('/')   
    total = get_basket_total(basket)
    return render(request, 'html/checkout.html', {'basket' : basket, 'total' : total, "total_with_next_day":total+5})

# view for user account page
def user_account(request):
    orders = Order_Item.objects.filter(user = request.user).order_by("-date_placed")
    return render(request, 'html/user_account.html', {"orders":orders})

# update basket quantity when in basket (+ or - signs)
def change_basket_quantity(request):
    if request.POST:
        post= dict(request.POST.items())
        basket_item = Basket_Item.objects.filter(id =post['basket_item'] ) .first()
        if post['add'] == '1':
            basket_item.quantity+=1
        else:
            basket_item.quantity-=1
        basket_item.save()
        return JsonResponse({"success":True})
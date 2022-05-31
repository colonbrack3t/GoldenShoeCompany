
from django.urls import path, include
from . import views
urlpatterns = [
    path('sign_up', views.sign_up, name = "sign_up"),
    path('login', views.login, name="login"),
    path('log_out', views.log_out, name="log_out"),
    path('basket', views.basket, name="basket"),
    path('checkout', views.checkout, name = "checkout"),
    path('user_account', views.user_account, name='user_account'),
    path('change_basket_quantity',views.change_basket_quantity,name="change_basket_quantity"),
]
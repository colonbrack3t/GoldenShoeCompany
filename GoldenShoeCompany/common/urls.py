
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.main_page, name = "main_page"),
    path('men/',views.men_page, name = "men"),
    

]
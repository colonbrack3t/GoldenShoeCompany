
from django.urls import path, include
from . import views
urlpatterns = [
    path('fetching', views.fetch_products, name = "fetch_products"),
    path('<int:id>', views.single_product_page, name = "single_product_page")
]
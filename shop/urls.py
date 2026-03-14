from django.urls import path
from . import views

urlpatterns = [
    path('products', views.products, name='products'),
    path('cart', views.get_cart, name='get_cart'),
    path('cart/add', views.add_to_cart, name='add_to_cart'),
    path('cart/remove', views.remove_from_cart, name='remove_from_cart'),
    path('cart/checkout', views.checkout, name='checkout'),
]

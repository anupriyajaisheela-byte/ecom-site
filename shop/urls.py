from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # Serve the single-page frontend
    path('', TemplateView.as_view(template_name='index.html'), name='home'),

    # API endpoints used by the frontend JS
    path('api/products', views.products, name='products'),
    path('api/cart', views.get_cart, name='get_cart'),
    path('api/cart/add', views.add_to_cart, name='add_to_cart'),
    path('api/cart/remove', views.remove_from_cart, name='remove_from_cart'),
    path('api/cart/checkout', views.checkout, name='checkout'),
]
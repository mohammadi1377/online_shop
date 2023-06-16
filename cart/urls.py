from django.urls import path
from .views import cartView, cart_length

urlpatterns = [
    path('cart/', cartView, name='cart'),
    path('cart/length/', cart_length, name='cart_length'),
]

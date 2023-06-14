from django.urls import path
from .views import cartView


urlpatterns = [
    path('cart/', cartView, name='cart'),
]

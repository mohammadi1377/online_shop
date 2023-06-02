from django.urls import path
from .views import CartView, CartAddView, CartRemoveView, ClearCartView, CartMinesView

app_name = 'cart'

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>/', CartAddView.as_view(), name='add'),
    path('cart/mines/<int:product_id>/', CartMinesView.as_view(), name='mines'),
    path('cart/remove/<int:product_id>/', CartRemoveView.as_view(), name='remove'),
    path('clear/', ClearCartView.as_view(), name='clear'),
]

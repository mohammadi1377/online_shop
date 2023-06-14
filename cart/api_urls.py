from django.urls import path
from .api_views import CartView, ClearCartView

app_name = 'api'

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('<int:product_id>/', CartView.as_view(), name='cart-product'),
    path('clear/', ClearCartView.as_view(), name='clear'),

]


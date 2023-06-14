
from django.urls import path
from .api_views import OrderCreateView, OrderDetailView, UpdateStatusView

app_name = 'orders'

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('details/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('update_status/<int:pk>/', UpdateStatusView.as_view(), name='update_status'),
]

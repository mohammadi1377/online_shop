from django.urls import path
from .views import OrderCreateView, OrderDetailView, UpdateStatusView

app_name = 'orders'
urlpatterns = [
	path('create/', OrderCreateView.as_view(), name='order_create'),
	path('detail/<int:order_id>/', OrderDetailView.as_view(), name='order_detail'),
	path('orders/<int:order_id>/update_status/', UpdateStatusView.as_view(), name='update_status'),
]
from django.urls import path
from .views import order


urlpatterns = [
    path('order/detail/<int:id>/', order, name='order_detail'),
    # path('orders/<int:pk>/update_status/', UpdateStatusView.as_view(), name='update_status'),
]

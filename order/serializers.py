from rest_framework import serializers
from .models import Orders, OrderItems
from customers.models import User


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ['id', 'order', 'product', 'count']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['get_full_name']


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    order_items = OrderItemsSerializer(many=True, read_only=True)

    class Meta:
        model = Orders
        fields = ['id', 'customer', 'address', 'status', 'order_items']



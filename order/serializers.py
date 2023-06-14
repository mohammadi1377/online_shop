from rest_framework import serializers

from product.models import Product
from .models import Orders, OrderItems
from customers.models import User,Address


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price', 'discount_price', 'total_discount']


class OrderItemsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

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


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'



from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Orders, OrderItems
from .serializers import OrderSerializer, OrderItemsSerializer, AddressSerializer
from cart.cart import Cart
from customers.models import Address
from product.models import Product
from rest_framework import status


class OrderCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    queryset = Orders.objects.all()

    def get_object(self):
        return self.request.user

    # def get(self, request, *args, **kwargs):
    #     customer = self.get_object()
    #     addresses = Address.objects.filter(customer=customer)
    #     serializer = AddressSerializer(addresses, many=True)
    #     return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        customer = self.get_object()
        address = Address.objects.filter(customer=customer).first()
        # addresses = Address.objects.filter(customer=customer).all()

        # Check stock availability for all products in the cart
        insufficient_stock = False
        for item in cart:
            product_data = item['product']
            product = get_object_or_404(Product, pk=product_data['pk'])
            quantity = item['quantity']
            if quantity > product.stock:
                insufficient_stock = True
                break

        if insufficient_stock:
            return Response({'error': 'موجودی کافی نیست'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the order instance
        order = Orders.objects.create(customer=customer, address=address)

        for item in cart:
            product_data = item['product']
            product = get_object_or_404(Product, pk=product_data['pk'])
            quantity = item['quantity']

            if quantity <= product.stock:
                OrderItems.objects.create(order=order, product=product, count=quantity)
                product.stock -= quantity
                product.save()

        cart.clear()
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UpdateStatusView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = True
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

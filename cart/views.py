# from django.shortcuts import render, get_object_or_404, redirect
# from django.views import View
# from .cart import Cart
# from product.models import Product
#
#
# class CartView(View):
# 	def get(self, request):
# 		cart = Cart(request)
# 		return render(request, 'cart.html', {'cart': cart})
#
#
# class CartAddView(View):
# 	def get(self, request, product_id):
# 		cart = Cart(request)
# 		product = get_object_or_404(Product, id=product_id)
# 		cart.add(product, quantity=1)
# 		return redirect('cart:cart')
#
#
# class CartMinesView(View):
# 	def get(self, request, product_id):
# 		cart = Cart(request)
# 		product = get_object_or_404(Product, id=product_id)
# 		cart.add(product, quantity=-1)
# 		return redirect('cart:cart')
#
#
# class CartRemoveView(View):
# 	def get(self, request, product_id):
# 		cart = Cart(request)
# 		product = get_object_or_404(Product, id=product_id)
# 		cart.remove(product)
# 		return redirect('cart:cart')
#
#
# class ClearCartView(View):
# 	def get(self, request):
# 		cart = Cart(request)
# 		cart.clear()
# 		return redirect('cart:cart')
#
#
from django.views import View
from product.models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import CartSerializer
from .cart import Cart


class CartView(APIView):
    def get(self, request):
        cart = Cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class CartAddView(APIView):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.add(product, quantity=1)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class CartMinesView(APIView):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.add(product, quantity=-1)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class CartRemoveView(APIView):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class ClearCartView(APIView):
    def get(self, request):
        cart = Cart(request)
        cart.clear()
        serializer = CartSerializer(cart)
        return Response(serializer.data)

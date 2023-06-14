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
# 	def post(self, request, product_id):
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
#
# 		if cart.get_product_quantity(product) == 0:
# 			cart.remove(product)
#
# 		return redirect('cart:cart')
#
# 	def post(self, request, product_id):
# 		cart = Cart(request)
# 		product = get_object_or_404(Product, id=product_id)
# 		cart.add(product, quantity=-1)
#
# 		if cart.get_product_quantity(product) == 0:
# 			cart.remove(product)
#
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
from django.shortcuts import get_object_or_404, render
from .serializers import CartSerializer
from .cart import Cart


class CartView(APIView):
	def get(self, request):
		cart = Cart(request)
		serializer = CartSerializer(cart)
		return Response(serializer.data)

	def post(self, request, product_id):
		cart = Cart(request)
		product = get_object_or_404(Product, id=product_id)
		quantity = request.data.get('quantity', 1)
		cart.add(product, quantity=quantity)
		serializer = CartSerializer(cart)
		return Response(serializer.data)

	def patch(self, request, product_id):
		cart = Cart(request)
		product = get_object_or_404(Product, id=product_id)
		action = request.data.get('action')

		if action == 'increment':
			cart.add(product, quantity=1)
		elif action == 'decrement':
			quantity = cart.cart.get(str(product.id), {}).get('quantity', 0)
			if quantity > 1:
				cart.add(product, quantity=-1)
			else:
				cart.remove(product)

		total_price = cart.get_total_price()
		total_discount = cart.get_total_discount()
		total_price_discount = total_price - total_discount

		serializer = CartSerializer(cart)
		return Response({
			'cart': serializer.data,
			'total_price': total_price,
			'total_discount': total_discount,
			'total_price_discount': total_price_discount
		})

	def delete(self, request, product_id=None):
		cart = Cart(request)

		if product_id is not None:
			product = get_object_or_404(Product, id=product_id)
			cart.remove(product)
		else:
			cart.clear()

		serializer = CartSerializer(cart)
		return Response(serializer.data)


class ClearCartView(APIView):
	def delete(self, request):
		cart = Cart(request)
		cart.clear()
		serializer = CartSerializer(cart)
		return Response(serializer.data)

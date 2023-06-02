from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .cart import Cart
from product.models import Product


class CartView(View):
	def get(self, request):
		cart = Cart(request)
		return render(request, 'cart.html', {'cart': cart})


class CartAddView(View):
	def get(self, request, product_id):
		cart = Cart(request)
		product = get_object_or_404(Product, id=product_id)
		cart.add(product, quantity=1)
		return redirect('cart:cart')


class CartMinesView(View):
	def get(self, request, product_id):
		cart = Cart(request)
		product = get_object_or_404(Product, id=product_id)
		cart.add(product, quantity=-1)
		return redirect('cart:cart')


class CartRemoveView(View):
	def get(self, request, product_id):
		cart = Cart(request)
		product = get_object_or_404(Product, id=product_id)
		cart.remove(product)
		return redirect('cart:cart')


class ClearCartView(View):
	def get(self, request):
		cart = Cart(request)
		cart.clear()
		return redirect('cart:cart')


# class PlusCartView(View):
# 	def get(self, request, cart_id):
# 		cp = get_object_or_404(Cart, id=cart_id)
# 		cp.quantity += 1
# 		cp.save()
# 		return redirect('store:cart')
#
#
# class MinusCartView(View):
# 	def get(self, request, cart_id):
# 		cp = get_object_or_404(Cart, id=cart_id)
# 		# Remove the Product if the quantity is already 1
# 		if cp.quantity == 1:
# 			cp.delete()
# 		else:
# 			cp.quantity -= 1
# 			cp.save()
# 		return redirect('store:cart')

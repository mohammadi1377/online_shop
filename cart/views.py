from django.http import JsonResponse
from django.shortcuts import render

from cart.cart import Cart


def cartView(request):
	return render(request, "cart.html")


def cart_length(request):
	cart = Cart(request)
	cart_len = len(cart)
	return JsonResponse({'cart_len': cart_len})

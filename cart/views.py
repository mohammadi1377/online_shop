from django.shortcuts import render


def cartView(request):
	return render(request, "cart.html")


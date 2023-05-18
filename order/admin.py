from django.contrib import admin
from .models import Orders, OrderItems, Payment, Carts, CartItems

admin.site.register([Carts, CartItems, Orders, OrderItems, Payment])

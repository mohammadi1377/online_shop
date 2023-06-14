from django.contrib import admin
<<<<<<< HEAD
from .models import Orders, OrderItems, Payment, Carts, CartItems

admin.site.register([Carts, CartItems, Orders, OrderItems, Payment])
=======
from .models import Orders, OrderItems

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status']
    list_filter = ['status']
    search_fields = ['customer']
    ordering = ['id']

    @staticmethod
    def customer(obj):
        return obj.customer.get_full_name()


@admin.register(OrderItems)
class OrderItems(admin.ModelAdmin):
    list_display = ['id', 'product', 'item_cost']
    list_filter = ['product']
    search_fields = ['product']
    ordering = ['id']

    @staticmethod
    def product(obj):
        return obj.product.name
>>>>>>> develop

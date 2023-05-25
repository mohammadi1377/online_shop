from django.contrib import admin
from .models import User, Address, Comment


@admin.register(User)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_full_name', 'email', 'phone_number', 'discount', 'get_jalai_date']
    list_filter = ['role','discount']
    search_fields = ['get_full_name', 'email', 'discount']
    ordering = ['id']

    @staticmethod
    def discount(obj):
        return obj.discount.amount

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'state', 'city', 'postal_code','get_jalai_date']
    list_filter = ['customer', 'state']
    search_fields = ['customer', 'state']
    ordering = ['id']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'product', 'get_jalai_date']
    list_filter = ['created_at']
    search_fields = ['customer', 'product']
    ordering = ['id']

    @staticmethod
    def full_name(obj):
        return obj.customer.get_full_name
    full_name.short_description ="نام مشتری"

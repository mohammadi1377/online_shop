from django.contrib import admin
from .models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'stock', 'price', 'discount', 'get_jalai_date']
    list_filter = ['category']
    search_fields = ['name', 'discount']
    ordering = ['name']

    @staticmethod
    def discount(obj):
        return obj.discount.amount

    @staticmethod
    def category(obj):
        return obj.category.title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'discount', 'get_jalai_date']
    list_filter = ['title', 'discount']
    search_fields = ['title', 'discount']
    ordering = ['title']

    @staticmethod
    def discount(obj):
        return obj.discount.amount


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'get_jalai_date']
    list_filter = ['product']
    search_fields = ['product']
    ordering = ['id']


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'amount', 'status', 'get_jalai_date']
    list_filter = ['type']
    search_fields = ['status', 'type']
    ordering = ['id']




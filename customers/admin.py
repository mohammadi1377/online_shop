from django.contrib import admin
from .models import User, Address, Comment
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Permission
from .models import User


class CustomUserAdmin(BaseUserAdmin, admin.ModelAdmin):
    # Define the fields to be displayed in the User admin list
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser', 'get_full_name')

    # Define the fieldsets to be displayed in the User edit/create form
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissions', {'fields': ('role', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
        ('Status', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    # Define the filter options for the User admin list
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role')

    # Define the search fields for the User admin list
    search_fields = ('username', 'email', 'first_name', 'last_name')

    def save_model(self, request, obj, form, change):
        # Save the User instance
        super().save_model(request, obj, form, change)

        # Assign permissions based on the user's role
        permissions = []

        if obj.role == 'a':  # Admin user
            obj.is_superuser = True
            obj.user_permissions.set(Permission.objects.all())  # Set all permissions for admin users
        else:
            if obj.role == 'm':  # Product Manager
                permissions = [
                    'view_product', 'add_product', 'change_product', 'delete_product',
                    'view_category', 'add_category', 'change_category', 'delete_category',
                    'view_discount', 'add_discount', 'change_discount', 'delete_discount',
                ]
            elif obj.role == 'n':  # Observer
                permissions = ['view_product', 'view_category', 'view_discount']
            elif obj.role == 'o':  # Operator
                permissions = [
                    'view_customer', 'add_customer', 'change_customer', 'delete_customer',
                    'view_order', 'add_order', 'change_order', 'delete_order',
                    'view_address', 'add_address', 'change_address', 'delete_address',
                ]

            obj.user_permissions.set(Permission.objects.filter(codename__in=permissions))

    @staticmethod
    def discount(obj):
        return obj.discount.amount

admin.site.register(User, CustomUserAdmin)


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

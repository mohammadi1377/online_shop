from django.urls import path, include
from .views import HomeView, CategoryListView, ProductDetailView, CategoryDetailView, DiscountedCategoryListView, \
    DiscountedProductListView, ContactUsView

urlpatterns = [
    path('home/', CategoryListView.as_view(), name='home'),
    path('contact/', ContactUsView.as_view(), name='contact_us'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='category_detail'),
    path('product/<slug:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/discount/', DiscountedCategoryListView.as_view(), name='category_discount'),
    path('products/discount/', DiscountedProductListView.as_view(), name='product_discount'),

]

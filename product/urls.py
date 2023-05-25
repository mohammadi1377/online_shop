from django.urls import path, include
from .views import HomeView, CategoryListView, ProductDetailView, CategoryDetailView, DiscountedCategoryListView

urlpatterns = [
    path('home/', CategoryListView.as_view(), name='home'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='category_detail'),
    path('product/<slug:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/discount/', DiscountedCategoryListView.as_view(), name='category_discount'),
]

from django.urls import path, include
<<<<<<< HEAD
from product import views

urlpatterns = [
    path('jwellery_shope/', views.HomeView.as_view(), name='home'),
    # path('room_detail/<int:pk>/', views.RoomDetail.as_view(), name='room_detail'),
    # path('signup/', views.SignUp.as_view(), name='signup'),
    # path('accounts/profile/', views.profile, name='profile'),
    # path('reserve/', views.reserve_room, name='reserve'),
    # path('otp/<user_id>', views.OtpVlidate, name='otp'),
    # path('verify/', views.verify, name='verify'),
=======
from .views import HomeView, CategoryListView, ProductDetailView, CategoryDetailView, DiscountedCategoryListView, DiscountedProductListView

urlpatterns = [
    path('home/', CategoryListView.as_view(), name='home'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='category_detail'),
    path('product/<slug:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/discount/', DiscountedCategoryListView.as_view(), name='category_discount'),
    path('products/discount/', DiscountedProductListView.as_view(), name='product_discount'),
>>>>>>> develop

]

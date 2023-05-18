from django.urls import path, include
from product import views

urlpatterns = [
    path('jwellery_shope/', views.HomeView.as_view(), name='home'),
    # path('room_detail/<int:pk>/', views.RoomDetail.as_view(), name='room_detail'),
    # path('signup/', views.SignUp.as_view(), name='signup'),
    # path('accounts/profile/', views.profile, name='profile'),
    # path('reserve/', views.reserve_room, name='reserve'),
    # path('otp/<user_id>', views.OtpVlidate, name='otp'),
    # path('verify/', views.verify, name='verify'),

]

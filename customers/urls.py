from .views import RegisterView, LoginAPIView, LogoutAPIView, ProfileView, EditProfileView, AddressCreateView, \
	AddressDeleteView, Otp, Verification
from django.urls import path
from rest_framework_simplejwt.views import (
	TokenRefreshView,
)
from rest_framework_simplejwt import views as jwt_views

app_name = 'api'

urlpatterns = [
	path('register/', RegisterView.as_view(), name="register"),
	path('api/register/', RegisterView.as_view(), name='register'),
	path('login/django/', LoginAPIView.as_view(), name="login"),
	path('logout/<int:pk>', LogoutAPIView.as_view(), name="logout"),
    path('otp/', Otp.as_view(), name='otp'),
    path('verification/', Verification.as_view(), name='verification'),
	# path("api/token/", views.TokenObtainPairViewNew.as_view(), name="token-obtain"),
	path("api/token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token-obtain"),
	path('api/token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
	path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
	path('profile/edit/<int:pk>/', EditProfileView.as_view(), name='edit_profile'),
	path('add-address/<int:pk>', AddressCreateView.as_view(), name="add-address"),
	path('remove-address/<int:pk>/', AddressDeleteView.as_view(), name="remove-address"),

]

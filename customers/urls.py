from . import views
from django.urls import path
from rest_framework_simplejwt.views import (
	TokenRefreshView,
)
from rest_framework_simplejwt import views as jwt_views

app_name = 'api'

urlpatterns = [
	path('register/', views.RegisterView.as_view(), name="register"),
	path('api/register/', views.RegisterView.as_view(), name='register'),
	path('login/', views.LoginAPIView.as_view(), name="login"),
	path('logout/', views.LogoutAPIView.as_view(), name="logout"),
	# path("api/token/", views.TokenObtainPairViewNew.as_view(), name="token-obtain"),
	path("api/token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token-obtain"),
	path('api/token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
]

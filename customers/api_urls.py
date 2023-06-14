from .api_views import RegisterView, LoginAPIView, LogoutAPIView,  EditProfileView
from django.urls import path
from rest_framework_simplejwt import views as jwt_views

app_name = 'api'

urlpatterns = [
	path('register/', RegisterView.as_view(), name='register'),
	path('login/', LoginAPIView.as_view(), name="login"),
	path('logout/<int:pk>', LogoutAPIView.as_view(), name="logout"),
	# path("api/token/", views.TokenObtainPairViewNew.as_view(), name="token-obtain"),
	path("api/token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token-obtain"),
	path('api/token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
	path('profile/edit/<int:pk>/', EditProfileView.as_view(), name='edit_profile'),

]

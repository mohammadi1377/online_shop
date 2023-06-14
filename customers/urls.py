<<<<<<< HEAD
# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('login/', views.log_in, name='login'),
#     path('logout/', views.sign_out, name='logout'),
#     path('register/', views.register, name='register'),
# ]
=======
from django.urls import path
from . import views
from .views import Otp, AddressCreateView, AddressDeleteView, Verification, ProfileView

urlpatterns = [
	path("login/", views.login, name='login'),
	path("register/", views.register, name='register'),
	path('add-address/<int:pk>', AddressCreateView.as_view(), name="add-address"),
	path('remove-address/<int:pk>/', AddressDeleteView.as_view(), name="remove-address"),
	path('otp/', Otp.as_view(), name='otp'),
	path('verification/', Verification.as_view(), name='verification'),
	path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
]
>>>>>>> develop

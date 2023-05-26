from rest_framework import generics, permissions
from .serializers import RegisterSerializer, LoginSerializer, LogoutSerializer
from django.shortcuts import redirect, render
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse



class RegisterView(generics.GenericAPIView):
	serializer_class = RegisterSerializer

	def get(self, request):
		return render(request, "register.html", context={})

	def post(self, request):
		user = request.data
		serializer = self.serializer_class(data=user)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		# user_data = serializer.data
		# return Response(user_data, status=status.HTTP_201_CREATED)
		return redirect('/home/')


class LoginAPIView(generics.GenericAPIView):
	serializer_class = LoginSerializer

	def get(self, request):
		return render(request, "login.html", context={})

	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			user = serializer.validated_data['user']
			refresh = RefreshToken.for_user(user)
			access_token = refresh.access_token

			# Set the access token as a cookie
			response = HttpResponse()
			response.set_cookie('jwt', access_token, httponly=True)

			return redirect('home')
		else:
			messages.error(request, 'نام کاربری یا رمز عبور اشتباه است')
			return render(request, "login.html", context={})


class LogoutAPIView(generics.GenericAPIView):
	serializer_class = LogoutSerializer
	permission_classes = (permissions.IsAuthenticated,)

	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		# Clear the JWT tokens from cookies
		response = HttpResponse()
		response.delete_cookie('jwt')
		response.delete_cookie('refresh_token')

		return response

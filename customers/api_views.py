from rest_framework import generics, status
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render, redirect
from .serializers import UserSerializer
from .mixin import *
from rest_framework.response import Response


class RegisterView(generics.GenericAPIView):
	serializer_class = RegisterSerializer

	def post(self, request):
		user = request.data
		serializer = self.serializer_class(data=user)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data)


class LoginAPIView(generics.GenericAPIView):
	serializer_class = LoginSerializer

	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			user = serializer.validated_data['user']
			refresh = RefreshToken.for_user(user)
			access_token = refresh.access_token
			# Set the access token as a cookie
			response = HttpResponse(status=status.HTTP_200_OK)
			response.set_cookie('jwt', access_token, httponly=True)
			return response
		else:
			error_message = 'نام کاربری یا رمز عبور اشتباه است'
			return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(Jwt_Login_Mixin, APIView):
	def get(self, request, pk=None):
		url = reverse('home')
		response = HttpResponseRedirect(url)
		response.delete_cookie('jwt')
		return response


class EditProfileView(Jwt_Login_Mixin, APIView):
	serializer_class = UserSerializer

	def get_object(self):
		return self.request.user

	def get(self, request, *args, **kwargs):
		instance = self.get_object()
		serializer = self.serializer_class(instance)
		data = serializer.data
		return render(request, 'edit_profile.html', {'data': data})

	def put(self, request, *args, **kwargs):
		instance = self.get_object()
		serializer = self.serializer_class(instance, data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data)

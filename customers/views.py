import datetime
import re

from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.views import APIView
from .tasks import send_otp_email, send_otp_sms
from order.models import Orders
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from .forms import AddressForm, SendOTPForm, VerificationForm
from django.views.generic import CreateView, ListView, View, DetailView
from .models import Address
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from .serializers import UserSerializer
from .mixin import *
from rest_framework.response import Response
import redis
from django.contrib.auth import login


class RegisterView(generics.GenericAPIView):
	serializer_class = RegisterSerializer

	def get(self, request):
		return render(request, "register.html", context={})

	def post(self, request):
		user = request.data
		serializer = self.serializer_class(data=user)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return redirect('/home/')


class LoginAPIView(generics.GenericAPIView):
	serializer_class = LoginSerializer

	def get(self, request):
		return render(request, "login.html", context={})

	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			user = serializer.validated_data['user']
			# Authenticate the user
			refresh = RefreshToken.for_user(user)
			access_token = refresh.access_token
			# Set the access token as a cookie
			url = reverse('home')
			response = HttpResponseRedirect(url)
			response.set_cookie('jwt', access_token, httponly=True)
			return response
		else:
			messages.error(request, 'نام کاربری یا رمز عبور اشتباه است')
			return render(request, "login.html", context={})


class Otp(View):
	def get(self, request):
		form = SendOTPForm()
		return render(request, 'login_otp.html', {'form': form})

	def post(self, request):
		send_otp_email('f.mohamady1377@yahoo.com')
		print("______________")
		form = SendOTPForm(request.POST)
		print("//////////////")
		if form.is_valid():
			print("########", "none")
			user = None
			if re.match(r'[A-Za-z0-9]+[.-_]*[A-Za-z0-9]+@[A-Za-z0-9-]+\.[A-Z|a-z]{2,}',
						form.cleaned_data['mail_phone']):
				try:
					print("^^^^^zir try")
					user = User.objects.get(email=form.cleaned_data['mail_phone'])
					print(user, "()()()()")
				except User.DoesNotExist:
					pass
				if user:
					print("***********")
					send_otp_email.delay(form.cleaned_data['mail_phone'], 300)
					print("&&&&&&&&&77", send_otp_email)
					response = redirect('Verification')
					expiry_minutes = 5
			elif re.match(r'09(\d{9})$', form.cleaned_data['mail_phone']):
				try:
					user = User.objects.get(phone_number=form.cleaned_data['mail_phone'])
				except User.DoesNotExist:
					pass
				if user:
					send_otp_sms.delay(form.cleaned_data['mail_phone'], 60)

			if user:
				# expires = datetime.datetime.now() + datetime.timedelta(minutes=expiry_minutes)
				response.set_cookie('user_email_or_phone_number', form.cleaned_data['mail_phone'])
				return response

		return render(request, 'verification.html', {'form': form})


class Verification(View):
	def get(self, request):
		form = VerificationForm()
		return render(request, "verification.html", {"form": form})

	def post(self, request):
		form = VerificationForm(request.POST)
		if form.is_valid():
			verfication_code = form.cleaned_data['verfication_code']
			r = redis.Redis(Host='localhost', port=6379, db=0)
			user_identifier = request.COOKIEs.get('user_email_or_phone', None)
			storedcode = r.get(user_identifier).decode()
			if verfication_code == storedcode:
				condition1 = Q(email=user_identifier)
				condition2 = Q(phone=user_identifier)
				user = User.objects.filter(condition1 | condition2).first()
				if user:
					login(request, user)
				return redirect('home')
		return render(request, "verification.html", {"form": form})


class LogoutAPIView(Jwt_Login_Mixin, APIView):
	def get(self, request, pk=None):
		url = reverse('home')
		response = HttpResponseRedirect(url)
		response.delete_cookie('jwt')
		return response


class ProfileView(Jwt_Login_Mixin, DetailView):
	model = User
	template_name = 'profile.html'
	context_object_name = 'user'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = self.get_object()
		addresses = Address.objects.filter(customer=user)
		orders = Orders.objects.filter(customer=user)
		context['addresses'] = addresses
		context['orders'] = orders
		return context


class EditProfileView(Jwt_Login_Mixin, APIView):
	serializer_class = UserSerializer

	def get_object(self):
		return self.request.user

	def get(self, request, *args, **kwargs):
		instance = self.get_object()
		serializer = self.serializer_class(instance)
		return Response(serializer.data)

	def put(self, request, *args, **kwargs):
		instance = self.get_object()
		serializer = self.serializer_class(instance, data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data)


class AddressCreateView(LoginRequiredMixin, CreateView):
	model = Address
	form_class = AddressForm
	template_name = 'add_address.html'

	def get_success_url(self):
		pk = self.kwargs['pk']
		return reverse('api:profile', kwargs={'pk': pk})

	def form_valid(self, form):
		form.instance.customer = self.request.user
		messages.success(self.request, "آدرس با موفقیت ثبت شد.")
		return super().form_valid(form)


class AddressListView(LoginRequiredMixin, ListView):
	model = Address
	template_name = 'profile.html'
	context_object_name = 'addresses'

	def get_queryset(self):
		return self.model.objects.filter(customer=self.request.user)


class AddressDeleteView(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		address_id = self.kwargs.get('pk')
		try:
			address = Address.objects.get(id=address_id)
			return render(request, 'profile.html', {'address': address})
		except Address.DoesNotExist:
			messages.error(request, 'آدرس پیدا نشد.')
			return redirect('api:profile')

	def post(self, request, *args, **kwargs):
		address_id = self.kwargs.get('pk')
		try:
			address = Address.objects.get(id=address_id)
			address.delete()
			messages.success(request, 'آدرس با موفقیت حذف شد.')
		except Address.DoesNotExist:
			messages.error(request, 'آدرس پیدا نشد.')

		return redirect(reverse_lazy('api:profile', kwargs={'pk': request.user.pk}))

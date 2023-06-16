from django.shortcuts import render
import re
from django.db.models import Q
from order.models import Orders
from .tasks import send_otp_email, send_otp_sms
from .forms import AddressForm, SendOTPForm, VerificationForm
import redis
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, View, DetailView
from .models import Address
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from .mixin import *


def login(request):
	return render(request, "login.html")


class Otp(View):
	def get(self, request):
		form = SendOTPForm()
		return render(request, 'login_otp.html', {'form': form})

	def post(self, request):
		form = SendOTPForm(request.POST)
		if form.is_valid():
			user = None
			mail_phone = form.cleaned_data['mail_phone']
			if re.match(r'^[A-Za-z0-9]+[-._]*[A-Za-z0-9]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}$', mail_phone):
				try:
					user = User.objects.get(email=mail_phone)
				except User.DoesNotExist:
					pass
				if user:
					send_otp_email.delay(mail_phone)
					response = redirect('verification')
					response.set_cookie('user_email_or_phone', mail_phone)
					return response
			elif re.match(r'09(\d{9})$', mail_phone):
				try:
					user = User.objects.get(phone_number=mail_phone)
				except User.DoesNotExist:
					pass
				if user:
					send_otp_sms.delay(mail_phone, 60)
					response = redirect('verification')
					response.set_cookie('user_email_or_phone', mail_phone)
					return response

		return render(request, 'verification.html', {'form': form})


class Verification(View):
	def get(self, request):
		form = VerificationForm()
		return render(request, "verification.html", {"form": form})

	def post(self, request):
		form = VerificationForm(request.POST)
		if form.is_valid():
			verification_code = form.cleaned_data['verification_code']
			user_identifier = request.COOKIES.get('user_email_or_phone')
			r = redis.Redis(host='localhost', port=6379, db=0)
			stored_code = r.get(user_identifier).decode()
			if verification_code == stored_code:
				user = User.objects.filter(Q(email=user_identifier) | Q(phone_number=user_identifier)).first()
				if user:
					refresh = RefreshToken.for_user(user)
					access_token = refresh.access_token
					# Set the access token as a cookie
					url = reverse('home')
					response = HttpResponseRedirect(url)
					response.set_cookie('jwt', access_token, httponly=True)
					return response

		return render(request, "verification.html", {"form": form})


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


class AddressCreateView(LoginRequiredMixin, CreateView):
	model = Address
	form_class = AddressForm
	template_name = 'add_address.html'

	def get_success_url(self):
		pk = self.kwargs['pk']
		return reverse('profile', kwargs={'pk': pk})

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

		return redirect(reverse_lazy('profile', kwargs={'pk': request.user.pk}))


def register(request):
	return render(request, "register.html")



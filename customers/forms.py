from django import forms
from django.forms import fields
from .models import User, Address
from django.contrib.auth.forms import UserChangeForm


class ProfileForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'phone_number', 'email']


class AddressForm(forms.ModelForm):
	class Meta:
		model = Address
		fields = ['state', 'city', 'postal_code', 'address']


class SendOTPForm(forms.Form):
	mail_phone = forms.CharField(error_messages={
		'required':'وارد کردن این فیلد الزامی',
		'invalid':'شماره همراه یا ایمیل معتبر نمی باشد.'
	})


class VerificationForm(forms.Form):
	verfication_code = forms.CharField(max_length=6,error_messages={
		'required': 'وارد کردن این فیلد الزامی',
		'max_length':'کد وارد شده بیش از حد مجاز می باشد.'
	})

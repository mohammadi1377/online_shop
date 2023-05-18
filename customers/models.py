from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator
from django.db import models
from core.models import BaseModel


class User(BaseModel, AbstractUser):
	choice = (('a', 'ادمین'), ('c', 'مشتری'), ('n', 'ناظر'), ('m', 'مدیر محصولات'), ('o', 'اپراتور'))
	role = models.CharField(choices=choice, max_length=1, null=True, blank=True, default='u')
	phone_regex = RegexValidator(regex=r'09(\d{9})$',
								 message='Enter a valid mobile number. This value may contain only numbers.')
	phone_number = models.CharField(validators=[phone_regex], max_length=11, blank=True, verbose_name="شماره موبایل")
	# groups = models.ManyToManyField(Group, related_name='custom_users', blank=True)
	# user_permissions = models.ManyToManyField(Permission, related_name='custom_users', blank=True)

	@property
	def get_full_name(self):
		return f'{self.first_name} {self.last_name}'

	class Meta:
		verbose_name = "کاربر"
		verbose_name_plural = "کاربر"


class Address(BaseModel):
	customer = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='addresses',
		related_query_name='address',
	)
	state = models.CharField(max_length=150, verbose_name="کشور")
	city = models.CharField(max_length=150, verbose_name="شهر")
	postal_code = models.CharField(verbose_name=('کد پستی'), max_length=10, null=True, blank=True)
	address = models.TextField(verbose_name="آدرس")

	def __str__(self):
		return f'{self.customer.get_full_name}, {self.state}, {self.city}'

	class Meta:
		verbose_name = "آدرس"
		verbose_name_plural = "آدرس"



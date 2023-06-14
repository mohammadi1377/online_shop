from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator
from django.db import models
from core.models import BaseModel
<<<<<<< HEAD
=======
from product.models import Discount, Product
from rest_framework_simplejwt.tokens import RefreshToken
>>>>>>> develop


class User(BaseModel, AbstractUser):
	choice = (('a', 'ادمین'), ('c', 'مشتری'), ('n', 'ناظر'), ('m', 'مدیر محصولات'), ('o', 'اپراتور'))
	role = models.CharField(choices=choice, max_length=1, null=True, blank=True, default='u')
	phone_regex = RegexValidator(regex=r'09(\d{9})$',
								 message='Enter a valid mobile number. This value may contain only numbers.')
	phone_number = models.CharField(validators=[phone_regex], max_length=11, blank=True, verbose_name="شماره موبایل")
<<<<<<< HEAD
	# groups = models.ManyToManyField(Group, related_name='custom_users', blank=True)
	# user_permissions = models.ManyToManyField(Permission, related_name='custom_users', blank=True)
=======
	discount = models.ForeignKey(Discount, related_name='customer_discount', verbose_name="تخفیف کاربر",
								 on_delete=models.CASCADE, null=True, blank=True)

	# USERNAME_FIELD = 'email'
>>>>>>> develop

	@property
	def get_full_name(self):
		return f'{self.first_name} {self.last_name}'

	class Meta:
		verbose_name = "کاربر"
		verbose_name_plural = "کاربر"

<<<<<<< HEAD

class Address(BaseModel):
	customer = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='addresses',
		related_query_name='address',
	)
=======
	# def tokens(self):
	# 	refresh = RefreshToken.for_user(self)
	# 	return {
	# 		'refresh': str(refresh),
	# 		'access': str(refresh.access_token)
	# 	}


class Address(BaseModel):
	customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', related_query_name='address')
>>>>>>> develop
	state = models.CharField(max_length=150, verbose_name="کشور")
	city = models.CharField(max_length=150, verbose_name="شهر")
	postal_code = models.CharField(verbose_name=('کد پستی'), max_length=10, null=True, blank=True)
	address = models.TextField(verbose_name="آدرس")

	def __str__(self):
		return f'{self.customer.get_full_name}, {self.state}, {self.city}'

	class Meta:
		verbose_name = "آدرس"
		verbose_name_plural = "آدرس"


<<<<<<< HEAD
=======
class Comment(BaseModel):
	customer = models.ForeignKey(User, verbose_name="مشتری", on_delete=models.CASCADE)
	text = models.TextField(verbose_name='نظر', max_length=100)
	product = models.ForeignKey(Product, verbose_name="محصول", related_name='comment', on_delete=models.CASCADE)

	class Meta:
		verbose_name = "نظر"
		verbose_name_plural = 'نظرات'
		ordering = ['created_at']

	def __str__(self):
		return f"{self.customer.get_full_name}, {self.product.name}"
>>>>>>> develop

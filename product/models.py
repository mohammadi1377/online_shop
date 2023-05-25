from django.db import models
from core.models import BaseModel
from django.utils.text import slugify
from django.core.exceptions import ValidationError


class Discount(BaseModel):
	choice = (('c', 'نقدی'), ('p', 'درصدی'))
	type = models.CharField(choices=choice, max_length=1, null=True, blank=True, verbose_name='نوع تخفیف')
	amount = models.IntegerField(verbose_name='تخفیف')
	status = models.BooleanField(default=False)

	class Meta:
		verbose_name = "تخفیف"
		verbose_name_plural = 'تخفیف'

	def __str__(self):
		return str(self.amount)

	def clean(self):
		if self.type == 'p':  # Percentage discount
			if self.amount < 0 or self.amount > 100:
				raise ValidationError("Amount must be between 0 and 100 for percentage discounts.")
		elif self.type == 'c':  # Cash discount
			if self.amount < 0:
				raise ValidationError("Amount cannot exceed the price of the product for cash discounts.")

	def save(self, *args, **kwargs):
		self.full_clean()  # Perform validation before saving
		super().save(*args, **kwargs)


class Category(BaseModel):
	title = models.CharField(max_length=50, verbose_name="عنوان دسته بندی")
	slug = models.SlugField(max_length=200, verbose_name="اسلاگ", editable=False)
	image = models.ImageField(upload_to='category', blank=True, null=True, verbose_name="تصویر دسته بندی")
	category_parent = models.ForeignKey("self", verbose_name='دسته بندی اصلی', null=True, blank=True,
										related_name='sub_category', on_delete=models.CASCADE)
	discount = models.ForeignKey(Discount, related_name='category_discount', verbose_name="تخفیف دسته بندی",
								 on_delete=models.CASCADE, null=True, blank=True)

	class Meta:
		verbose_name = "دسته بندی محصولات"
		verbose_name_plural = 'دسته بندی محصولات'
		ordering = ('created_at',)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super().save(*args, **kwargs)

	def __str__(self):
		return self.title


class Product(BaseModel):
	name = models.CharField(max_length=150, verbose_name="نام محصول")
	slug = models.SlugField(max_length=200, verbose_name="اسلاگ", editable=False)
	short_description = models.TextField(verbose_name="مشخصات")
	detail_description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
	category = models.ForeignKey(Category, verbose_name="دسته بندی محصول", related_name='category_product',
								 on_delete=models.CASCADE)
	price = models.IntegerField(verbose_name='قیمت')
	stock = models.IntegerField('موجودی', default=0)
	discount = models.ForeignKey(Discount, related_name='product_discount', verbose_name="تخفیف محصول",
								 on_delete=models.CASCADE, null=True, blank=True)

	class Meta:
		verbose_name = "محصول"
		verbose_name_plural = 'محصول'
		ordering = ('created_at',)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super().save(*args, **kwargs)

	def __str__(self):
		return self.name

	@property
	def discount_price(self):
		# Calculate product discount
		product_discount = 0
		if self.discount:
			if self.discount.type == 'c':  # Cash discount
				product_discount += self.discount.amount
			elif self.discount.type == 'p':  # Percentage discount
				product_discount += (self.price * self.discount.amount) / 100

		# Calculate category discount
		category_discount = 0
		if self.category.discount:
			if self.category.discount.type == 'c':  # Cash discount
				category_discount += self.category.discount.amount
			elif self.category.discount.type == 'p':
				category_discount += (self.price * self.category.discount.amount) / 100

		# Calculate total discount
		total_discount = product_discount + category_discount

		# Calculate discounted price
		discounted_price = self.price - total_discount

		# Check if discounted price is negative
		if discounted_price < 0:
			raise ValueError("Discounted price cannot be negative.")

		# Check if total discount is greater than 100%
		if total_discount > self.price:
			raise ValueError("Total discount cannot exceed the price of the product.")

		return discounted_price


class Image(BaseModel):
	product = models.ForeignKey(Product, related_name='product_image', verbose_name='محصول', on_delete=models.CASCADE,
								null=True, blank=True)
	image = models.ImageField(upload_to='product', blank=True, null=True, verbose_name="تصویر")

	class Meta:
		verbose_name = "تصویر"
		verbose_name_plural = 'تصویر'

# def __str__(self):
#     return self.product

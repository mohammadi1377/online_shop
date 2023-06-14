<<<<<<< HEAD
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from core.models import BaseModel
from customers.models import User, Address
from product.models import Product


# ------------سبد خرید------------
class Carts(BaseModel):
	customer = models.ForeignKey(User, verbose_name="مشتری", on_delete=models.CASCADE)
	product = models.ManyToManyField(Product, through='CartItems', verbose_name="محصول")

	class Meta:
		verbose_name = "سبد خرید"
		verbose_name_plural = "سبد خرید"

	def __str__(self):
		return f"{self.customer.get_full_name}سبد "


# ------------اجزا سبد خرید------------
class CartItems(models.Model):
	cart = models.ForeignKey(Carts, related_name='order_item', verbose_name="محتویات سبد خرید", on_delete=models.CASCADE)
	count = models.IntegerField("Count")
	product = models.ForeignKey(Product, verbose_name='محصول', on_delete=models.CASCADE)

	class Meta:
		verbose_name = "محتویات سبد خرید"
		verbose_name_plural = "محتویات سبد خرید"

	def __str__(self) -> str:
		return f"{self.product.name}"


# ------------فاکتور------------
class Orders(BaseModel):
	customer = models.ForeignKey(User, verbose_name="مشتری", on_delete=models.CASCADE)
	address = models.ForeignKey(Address, verbose_name="آدرس", on_delete=models.CASCADE)
	product = models.ManyToManyField(Product, through='OrderItems', verbose_name="محصول")
	STATUS = [
		(1, 'در انتظار پرداخت'),
		(2, 'پرداخت شده'),
		(3, 'ارسال شده'),
		(4, 'تکمیل شده'),
	]
	status = models.IntegerField(("وضعیت"), choices=STATUS, default=3)
	discount = models.IntegerField(blank=True, null=True, default=None)
=======
from django.db import models
from core.models import BaseModel
from customers.models import User, Address
from product.models import Product, Category


class Orders(BaseModel):
	customer = models.ForeignKey(User, verbose_name="مشتری", on_delete=models.CASCADE)
	address = models.ForeignKey(Address, verbose_name="آدرس", on_delete=models.CASCADE)
	status = models.BooleanField(default=False)
>>>>>>> develop

	class Meta:
		verbose_name = "فاکتور"
		verbose_name_plural = 'فاکتور'

	@property
<<<<<<< HEAD
	def get_total_price(self):
		total = sum(item.get_cost() for item in self.order_items.all())
		if self.discount:
			discount_price = (self.discount / 100) * total
			return int(total - discount_price)
		return total

	def __str__(self):
		return f"{self.customer.get_full_name}"

#----------------------------------------------------


class Coupon(models.Model):
	code = models.CharField(max_length=30, unique=True)
	valid_from = models.DateTimeField()
	valid_to = models.DateTimeField()
	discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
	status = models.BooleanField(default=False)

	def __str__(self):
		return self.code

	def is_valid(self):
		now = timezone.now()
		return self.valid_from <= now <= self.valid_to

# ------------اجزای داخل فاکتور------------
=======
	def total_price(self):
		order_items = self.order_items.all()
		total = sum(item.item_cost for item in order_items)
		return total

	@property
	def total_discount(self):
		order_items = self.order_items.all()
		total = sum(item.item_discount for item in order_items)
		return total

	def total_payment(self):
		return self.total_price - self.total_discount
>>>>>>> develop


class OrderItems(models.Model):
	order = models.ForeignKey(Orders, related_name='order_items', verbose_name="اقلام فاکتور", on_delete=models.CASCADE)
	count = models.IntegerField("تعداد")
	product = models.ForeignKey(Product, verbose_name=("محصول"), on_delete=models.CASCADE)

	class Meta:
		verbose_name = "اقلام فاکتور"
		verbose_name_plural = 'اقلام فاکتور'

	def __str__(self) -> str:
		return f"{self.product.name}"

<<<<<<< HEAD
	def get_cost(self):
		return self.count * self.product.price


class Payment(BaseModel):
	order = models.OneToOneField(Orders, verbose_name="فاکتور", on_delete=models.CASCADE)

	class Meta:
		verbose_name = "مبلغ"
		verbose_name_plural = 'مبلغ'
=======
	@property
	def item_cost(self):
		return self.count * self.product.price

	@property
	def item_discount(self):
		return self.product.total_discount * self.count
>>>>>>> develop

from django.db import models
from core.models import BaseModel
from customers.models import User, Address
from product.models import Product, Category


class Orders(BaseModel):
	customer = models.ForeignKey(User, verbose_name="مشتری", on_delete=models.CASCADE)
	address = models.ForeignKey(Address, verbose_name="آدرس", on_delete=models.CASCADE)
	status = models.BooleanField(default=False)

	class Meta:
		verbose_name = "فاکتور"
		verbose_name_plural = 'فاکتور'

	@property
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


class OrderItems(models.Model):
	order = models.ForeignKey(Orders, related_name='order_items', verbose_name="اقلام فاکتور", on_delete=models.CASCADE)
	count = models.IntegerField("تعداد")
	product = models.ForeignKey(Product, verbose_name=("محصول"), on_delete=models.CASCADE)

	class Meta:
		verbose_name = "اقلام فاکتور"
		verbose_name_plural = 'اقلام فاکتور'

	def __str__(self) -> str:
		return f"{self.product.name}"

	@property
	def item_cost(self):
		return self.count * self.product.price

	@property
	def item_discount(self):
		return self.product.total_discount * self.count

from django.db import models
from core.models import BaseModel
from customers.models import User, Address
from product.models import Product, Category


# ------------سبد خرید------------
# class Carts(BaseModel):
# 	customer = models.ForeignKey(User, verbose_name="مشتری", on_delete=models.CASCADE)
# 	# product = models.ManyToManyField(Product, through='CartItems', verbose_name="محصول")
#
# 	class Meta:
# 		verbose_name = "سبد خرید"
# 		verbose_name_plural = "سبد خرید"
#
# 	def __str__(self):
# 		return f"{self.customer.get_full_name}سبد "
#
#
# # ------------اجزا سبد خرید------------
# class CartItems(models.Model):
# 	cart = models.ForeignKey(Carts, related_name='order_item', verbose_name="محتویات سبد خرید", on_delete=models.CASCADE)
# 	count = models.IntegerField("Count")
# 	product = models.ForeignKey(Product, verbose_name='محصول', on_delete=models.CASCADE)
#
# 	class Meta:
# 		verbose_name = "محتویات سبد خرید"
# 		verbose_name_plural = "محتویات سبد خرید"
#
# 	def __str__(self) -> str:
# 		return f"{self.product.name}"


# ------------فاکتور-سبد خرید------------

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
		for item in order_items:
			if item.discount and item.category.discount and item.amount > item.category.amount:
				if item.type == 'c':
					total -= item.product.amount
				else:
					total -= (item.item_cost * item.amount) / 100
			elif item.discount and item.category.discount and item.amount < item.category.amount:
				if item.category.type == 'c':
					total -= item.category.amount
				else:
					total -= (item.item_cost * item.category.amount) / 100
			elif item.product.discount:
				if item.type == 'c':
					total -= item.amount
				else:
					total -= (item.item_cost * item.amount) / 100
			elif item.category.discount:
				if item.category.type == 'c':
					total -= item.category.amount
				else:
					total -= (item.item_cost * item.category.amount) / 100
		if self.customer.discount:
			if self.customer.discount.type == 'c':
				total -= self.customer.discount.amount
			else:
				total -= (total * self.customer.discount.amount) / 100
		return total




# ------------اجزای داخل فاکتور------------
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


#----------------------------------------------------




# class Payment(BaseModel):
# 	order = models.OneToOneField(Orders, verbose_name="فاکتور", on_delete=models.CASCADE)
#
# 	class Meta:
# 		verbose_name = "مبلغ"
# 		verbose_name_plural = 'مبلغ'

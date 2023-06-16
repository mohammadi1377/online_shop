from django.test import TestCase
from customers.models import User, Address
from product.models import Product, Category
from .models import Orders, OrderItems


class CartsModelTest(TestCase):
	def setUp(self):
		self.user = User.objects.create(username='sara2', email='test@example.com')

	def test_str_representation(self):
		cart = Orders(customer=self.user)
		self.assertEqual(str(cart), "فاکتور")


class CartItemsModelTest(TestCase):
	def setUp(self):
		self.user = User.objects.create(username='sara2', email='test@example.com')
		category = Category.objects.create(title='Test Category')
		self.product = Product.objects.create(name='Test Product', price=100, category=category)

	def test_str_representation(self):
		cart_item = OrderItems(count=1, product=self.product)
		self.assertEqual(str(cart_item), self.product.name)


class OrdersModelTest(TestCase):
	def setUp(self):
		self.user = User.objects.create(username='sara2', email='test@example.com')
		self.address = Address.objects.create(customer=self.user, state='Country1', city='City1', address='Address1')
		category = Category.objects.create(title='Test Category')
		self.product = Product.objects.create(name='Test Product', price=100, category=category)
		self.order = Orders.objects.create(customer=self.user, address=self.address)

	def test_str_representation(self):
		user = User.objects.create_user(username='user1', password='password123', first_name='John', last_name='Doe')
		address = Address.objects.create(customer=user, state='Country1', city='City1', address='Address1')
		order = Orders.objects.create(customer=self.user, address=address)
		self.assertEqual(str(order), self.user.get_full_name)

	def test_total_price(self):
		order_item = OrderItems.objects.create(order=self.order, count=1, product=self.product)
		self.order.save()  # Save the order instance
		self.assertEqual(self.order.total_price, self.product.price)


class OrderItemsModelTest(TestCase):
	def setUp(self):
		self.user = User.objects.create(username='sara2', email='test@example.com')
		self.address = Address.objects.create(customer=self.user, state='Country1', city='City1', address='Address1')
		self.order = Orders.objects.create(customer=self.user, address=self.address)
		category = Category.objects.create(title='Test Category')
		self.product = Product.objects.create(name='Test Product', price=100, category=category)

	def test_str_representation(self):
		order_item = OrderItems(order=self.order, count=1, product=self.product)
		self.assertEqual(str(order_item), self.product.name)

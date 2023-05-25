from django.test import TestCase
from customers.models import User, Address
from product.models import Product, Category
from .models import Carts, CartItems, Orders, OrderItems, Payment, Coupon
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


class CartsModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='sara2', email='test@example.com')
        self.cart = Carts.objects.create(customer=self.user)

    def test_str_representation(self):
        self.assertEqual(str(self.cart), " سبد ")


class CartItemsModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='sara2', email='test@example.com')
        self.cart = Carts.objects.create(customer=self.user)
        category = Category.objects.create(title='Test Category')
        self.product = Product.objects.create(name='Test Product', price=100, category=category)
        self.cart_item = CartItems.objects.create(cart=self.cart, count=1, product=self.product)

    def test_str_representation(self):
        self.assertEqual(str(self.cart_item), self.product.name)


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
        self.assertEqual(self.order.get_total_price, self.product.price)


class OrderItemsModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='sara2', email='test@example.com')
        self.address = Address.objects.create(customer=self.user, state='Country1', city='City1', address='Address1')
        self.order = Orders.objects.create(customer=self.user, address=self.address)
        category = Category.objects.create(title='Test Category')
        self.product = Product.objects.create(name='Test Product', price=100, category=category)
        self.order_item = OrderItems.objects.create(order=self.order, count=1, product=self.product)

    def test_str_representation(self):
        self.assertEqual(str(self.order_item), self.product.name)


class PaymentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='sara2', email='test@example.com')
        self.address = Address.objects.create(user=self.user, country='USA', state='California', city='Los Angeles', street_address='123 Test St')
        self.order = Orders.objects.create(customer=self.user, address=self.address)
        self.payment = Payment.objects.create(order=self.order)


class CouponModelTest(TestCase):
    def setUp(self):
        self.valid_from = timezone.now()
        self.valid_to = self.valid_from + timedelta(days=7)
        self.discount = 20
        self.code = "TESTCOUPON"
        self.coupon = Coupon.objects.create(
            code=self.code,
            valid_from=self.valid_from,
            valid_to=self.valid_to,
            discount=self.discount,
            status=True
        )

    def test_str_representation(self):
        self.assertEqual(str(self.coupon), self.code)

    def test_coupon_validity(self):
        self.assertTrue(self.coupon.is_valid())
        self.coupon.valid_from = self.valid_from + timedelta(days=1)
        self.assertFalse(self.coupon.is_valid())
        self.coupon.valid_from = self.valid_from
        self.coupon.valid_to = self.valid_to - timedelta(days=1)
        self.assertTrue(self.coupon.is_valid())

    def test_coupon_discount_range(self):
        self.coupon.discount = 50
        self.assertEqual(self.coupon.discount, 50)
        with self.assertRaises(ValidationError):
            self.coupon.discount = -10
            self.coupon.clean_fields()
        with self.assertRaises(ValidationError):
            self.coupon.discount = 200
            self.coupon.clean_fields()

    def test_coupon_status(self):
        self.assertTrue(self.coupon.status)
        self.coupon.status = False
        self.assertFalse(self.coupon.status)

    def test_coupon_discount_validation(self):
        invalid_coupon1 = Coupon.objects.create(
            code='INVALIDCODE1',
            valid_from=timezone.now(),
            valid_to=timezone.now() + timedelta(days=7),
            discount=-10,
            status=True
        )
        with self.assertRaises(ValidationError):
            invalid_coupon1.full_clean()

        invalid_coupon2 = Coupon.objects.create(
            code='INVALIDCODE2',
            valid_from=timezone.now(),
            valid_to=timezone.now() + timedelta(days=7),
            discount=110,
            status=True
        )
        with self.assertRaises(ValidationError):
            invalid_coupon2.full_clean()
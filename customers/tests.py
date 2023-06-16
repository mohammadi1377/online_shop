from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import User, Address


class UserTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', password='password123', first_name='John', last_name='Doe'
        )

    def test_user_creation(self):
        self.assertEqual(self.user1.username, 'user1')
        self.assertTrue(self.user1.check_password('password123'))
        self.assertEqual(self.user1.get_full_name, 'John Doe')

    def test_user_role_default(self):
        self.assertEqual(self.user1.role, 'u')

    def test_user_phone_validation(self):
        self.user1.phone_number = '09123456789'
        with self.assertRaises(ValidationError):
            self.user1.full_clean()


class AddressTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', password='password123', first_name='John', last_name='Doe'
        )
        self.address1 = Address.objects.create(
            customer=self.user1, state='Country1', city='City1', address='Address1'
        )

    def test_address_creation(self):
        self.assertEqual(self.address1.customer, self.user1)
        self.assertEqual(self.address1.state, 'Country1')
        self.assertEqual(self.address1.city, 'City1')
        self.assertEqual(self.address1.address, 'Address1')

    def test_address_string_representation(self):
        self.assertEqual(str(self.address1), 'John Doe, Country1, City1')

    def test_address_customer_relation(self):
        self.assertEqual(self.user1.addresses.first(), self.address1)

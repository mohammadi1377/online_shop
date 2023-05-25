from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from customers.models import User
from .models import Category, Product, Image, Comment


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            title='TestCategory',
        )

    def test_category_creation(self):
        category = Category.objects.create(
            title='TestCategory',
        )
        self.assertEqual(category.title, 'TestCategory')
        self.assertEqual(str(category), 'TestCategory')


class ProductModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            title='TestCategory',
        )

    def test_product_creation(self):
        product = Product.objects.create(
            name='TestProduct',
            short_description='Test short description',
            price=100.00,
            category=self.category
        )
        self.assertEqual(product.name, 'TestProduct')
        self.assertEqual(str(product), 'TestProduct')

    def test_discounted_price(self):
        product = Product.objects.create(
            name='TestProduct',
            short_description='Test short description',
            price=100.00,
            discount_type='p',
            discount_amount=10,
            category=self.category
        )
        self.assertEqual(product.discounted_price, 90)


class ImageModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            title='TestCategory',
        )
        self.product = Product.objects.create(
            name='TestProduct',
            short_description='Test short description',
            price=100.00,
            category=self.category
        )

    def test_image_creation(self):
        image_file = SimpleUploadedFile("test_image.jpg", b"test_content", content_type="image/jpeg")
        image = Image.objects.create(
            product=self.product,
            image=image_file
        )
        self.assertEqual(str(image), ' تصویرTestProduct')


class CommentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.category = Category.objects.create(
            title='TestCategory',
        )
        self.product = Product.objects.create(
            name='TestProduct',
            short_description='Test short description',
            price=100.00,
            category=self.category
        )

    def test_comment_creation(self):
        comment = Comment.objects.create(
            customer=self.user,
            text='Test comment',
            product=self.product
        )
        self.assertEqual(comment.text, 'Test comment')
        self.assertEqual(str(comment), f"{self.user.get_full_name}, {self.product.name}")
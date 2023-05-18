from django.db import models
from core.models import BaseModel
from customers.models import User
from django.utils.text import slugify


class Category(BaseModel):
    title = models.CharField(max_length=50, verbose_name="عنوان دسته بندی")
    slug = models.SlugField(max_length=200, verbose_name="اسلاگ", editable=False)
    category_parent = models.ForeignKey(
        "self", verbose_name='دسته بندی اصلی', null=True, blank=True, related_name='sub_category', on_delete=models.SET_DEFAULT,
        default="")
    choice = (('c', 'نقدی'), ('p', 'درصدی'), ('n','بدون تخفیف'))
    discount_type = models.CharField(choices=choice, max_length=1, null=True, blank=True, default='n', verbose_name='نوع تخفیف')
    discount_amount = models.DecimalField(verbose_name='تخفیف', max_digits=4, decimal_places=1, default=0)

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
    category = models.ForeignKey(Category, verbose_name="Product Categoy", on_delete=models.CASCADE)
    choice = (('c', 'نقدی'), ('p', 'درصدی'), ('n', 'بدون تخفیف'))
    discount_type = models.CharField(choices=choice, max_length=1, null=True, blank=True, default='n', verbose_name='نوع تخفیف')
    discount_amount = models.DecimalField(verbose_name='تخفیف', max_digits=4, decimal_places=1, default=0)
    price = models.DecimalField(verbose_name='قیمت', max_digits=50, decimal_places=2)
    stock = models.IntegerField('موجودی', default=0)

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
    def discounted_price(self):
        if self.discount_type == 'c':  # نقدی
            return self.price - self.discount_amount
        elif self.discount_type == 'p':  # درصدی
            discount = (self.price * self.discount_amount) / 100
            return self.price - discount
        else:  # بدون تخفیف
            return self.price


class Image(BaseModel):
    class Meta:
        verbose_name = "تصویر"
        verbose_name_plural = 'تصویر'

    product = models.ForeignKey(Product, verbose_name='محصول', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product', blank=True, null=True, verbose_name="تصویر")

    def __str__(self):
        return f' تصویر{self.product.name}'


class Comment(BaseModel):
    customer = models.ForeignKey(User, verbose_name="مشتری", on_delete=models.CASCADE)
    text = models.TextField(verbose_name='نظر', max_length=100)
    product = models.ForeignKey(Product, verbose_name="محصول", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = 'نظرات'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.customer.get_full_name}, {self.product.name}"

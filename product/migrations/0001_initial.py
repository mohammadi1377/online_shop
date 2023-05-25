# Generated by Django 4.2.1 on 2023-05-22 13:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated Date')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان دسته بندی')),
                ('slug', models.SlugField(editable=False, max_length=200, verbose_name='اسلاگ')),
                ('category_parent', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='sub_category', to='product.category', verbose_name='دسته بندی اصلی')),
            ],
            options={
                'verbose_name': 'دسته بندی محصولات',
                'verbose_name_plural': 'دسته بندی محصولات',
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated Date')),
                ('name', models.CharField(max_length=150, verbose_name='نام محصول')),
                ('slug', models.SlugField(editable=False, max_length=200, verbose_name='اسلاگ')),
                ('short_description', models.TextField(verbose_name='مشخصات')),
                ('detail_description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('price', models.DecimalField(decimal_places=2, max_digits=50, verbose_name='قیمت')),
                ('stock', models.IntegerField(default=0, verbose_name='موجودی')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.category', verbose_name='Product Categoy')),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصول',
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated Date')),
                ('image', models.ImageField(blank=True, null=True, upload_to='media', verbose_name='تصویر')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_image', to='product.category', verbose_name='دسته بندی')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_image', to='product.product', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'تصویر',
                'verbose_name_plural': 'تصویر',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated Date')),
                ('text', models.TextField(max_length=100, verbose_name='نظر')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='مشتری')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'نظر',
                'verbose_name_plural': 'نظرات',
                'ordering': ['created_at'],
            },
        ),
    ]

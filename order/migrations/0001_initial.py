<<<<<<< HEAD
# Generated by Django 4.2.1 on 2023-05-16 18:19
=======
# Generated by Django 4.2.1 on 2023-05-25 20:59
>>>>>>> develop

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
<<<<<<< HEAD
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0001_initial'),
        ('customers', '0001_initial'),
=======
        ('customers', '0001_initial'),
        ('product', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
>>>>>>> develop
    ]

    operations = [
        migrations.CreateModel(
<<<<<<< HEAD
            name='CartItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(verbose_name='Count')),
            ],
            options={
                'verbose_name': 'محتویات سبد خرید',
                'verbose_name_plural': 'محتویات سبد خرید',
=======
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated Date')),
                ('status', models.BooleanField(default=False)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.address', verbose_name='آدرس')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='مشتری')),
            ],
            options={
                'verbose_name': 'فاکتور',
                'verbose_name_plural': 'فاکتور',
>>>>>>> develop
            },
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(verbose_name='تعداد')),
<<<<<<< HEAD
=======
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='order.orders', verbose_name='اقلام فاکتور')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product', verbose_name='محصول')),
>>>>>>> develop
            ],
            options={
                'verbose_name': 'اقلام فاکتور',
                'verbose_name_plural': 'اقلام فاکتور',
            },
        ),
<<<<<<< HEAD
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated Date')),
                ('status', models.IntegerField(choices=[(1, 'در انتظار پرداخت'), (2, 'پرداخت شده'), (3, 'ارسال شده'), (4, 'تکمیل شده')], default=3, verbose_name='وضعیت')),
                ('discount_type', models.CharField(blank=True, choices=[('c', 'نقدی'), ('p', 'درصدی'), ('n', 'بدون تخفیف')], default='n', max_length=1, null=True, verbose_name='نوع تخفیف')),
                ('discount_amount', models.DecimalField(decimal_places=1, default=0, max_digits=4, verbose_name='تخفیف')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.address', verbose_name='آدرس')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='مشتری')),
                ('product', models.ManyToManyField(through='order.OrderItems', to='product.product', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'نظر',
                'verbose_name_plural': 'نظر',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated Date')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='order.orders', verbose_name='فاکتور')),
            ],
            options={
                'verbose_name': 'مبلغ',
                'verbose_name_plural': 'مبلغ',
            },
        ),
        migrations.AddField(
            model_name='orderitems',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_item', to='order.orders', verbose_name='اقلام فاکتور'),
        ),
        migrations.AddField(
            model_name='orderitems',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product', verbose_name='محصول'),
        ),
        migrations.CreateModel(
            name='Carts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated Date')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='مشتری')),
                ('product', models.ManyToManyField(through='order.CartItems', to='product.product', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'سبد خرید',
                'verbose_name_plural': 'سبد خرید',
            },
        ),
        migrations.AddField(
            model_name='cartitems',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_item', to='order.carts', verbose_name='محتویات سبد خرید'),
        ),
        migrations.AddField(
            model_name='cartitems',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product', verbose_name='محصول'),
        ),
=======
>>>>>>> develop
    ]

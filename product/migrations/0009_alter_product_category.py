# Generated by Django 4.2.1 on 2023-05-24 09:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_remove_category_is_deleted_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_product', to='product.category', verbose_name='دسته بندی محصول'),
        ),
    ]

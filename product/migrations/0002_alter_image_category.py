# Generated by Django 4.2.1 on 2023-05-22 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='category',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='category_image', to='product.category', verbose_name='دسته بندی'),
        ),
    ]

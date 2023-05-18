from django.contrib import admin
from .models import Comment, Category, Product, Image

admin.site.register([Comment, Category, Product, Image])

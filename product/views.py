from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views import generic
# from rest_framework_simplejwt.authentication import JWTAuthentication
from .forms import CommentForm
from .models import Product, Category, Discount


# from customers.models import User
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# from rest_framework.decorators import api_view, permission_classes, authentication_classes


class HomeView(TemplateView):
    template_name = 'home.html'


class CategoryListView(generic.ListView):
    model = Category
    template_name = 'home.html'
    context_object_name = 'categories'
    paginate_by = 6

    # def get_queryset(self):
    #     return Category.objects.filter(discount__status=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        discounts = Category.objects.filter(discount__status=True)
        context['discounts'] = discounts
        return context


class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = 'category_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        products = category.category_product.all().select_related('category')
        images = {}
        for product in products:
            product_image = product.product_image.first()
            images[product] = product_image
        context['images'] = images
        return context


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        comments = product.comment.all()
        details = product.short_description.split('-')
        images = product.product_image.all()
        context['comments'] = comments
        context['images'] = images
        context['details'] = details
        return context

    # @api_view(['GET', 'POST'])
    # @permission_classes((IsAuthenticated,))
    # @authentication_classes((JSONWebTokenAuthentication,))
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = self.get_object()
            comment.customer = self.request.user
            comment.save()
        else:
            return redirect('product_detail', pk=self.get_object().pk)


class DiscountedCategoryListView(generic.ListView):
    model = Category
    template_name = 'category_discount.html'
    context_object_name = 'categories'
    paginate_by = 3

    def get_queryset(self):
        return Category.objects.filter(discount__status=True)


class DiscountedProductListView(generic.ListView):
    model = Product
    template_name = 'discounted_products.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        # Get all products that themselves or their categories are discounted
        return Product.objects.filter(Q(discount__status=True) | Q(category__discount__status=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context['products']
        images = {}
        for product in products:
            product_image = product.product_image.first()
            images[product] = product_image
            context['images'] = images
        return context

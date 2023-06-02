from django.shortcuts import redirect, get_object_or_404, render
from django.http import HttpResponse
from django.views import View
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, TemplateView
from .models import Orders
from cart.cart import Cart
from customers.mixin import Jwt_Login_Mixin
from .models import Orders, OrderItems
from customers.models import User, Address
from product.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin


class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        customer = User.objects.get(pk=request.user.pk)
        address = Address.objects.get(customer=customer)

        # Check stock availability for all products in the cart
        insufficient_stock = False
        for item in cart:
            product = Product.objects.get(pk=item['product'].pk)
            quantity = item['quantity']
            if quantity > product.stock:
                insufficient_stock = True
                break

        if insufficient_stock:
            messages.error(request, 'موجودی کافی نیست')
            return HttpResponseRedirect(reverse('cart:cart'))  # Redirect to cart view

        # Create the order instance
        order = Orders.objects.create(customer=request.user, address=address)

        for item in cart:
            product = Product.objects.get(pk=item['product'].pk)
            quantity = item['quantity']

            if quantity <= product.stock:
                OrderItems.objects.create(order=order, product=product, count=quantity)
                product.stock -= quantity
                product.save()

        cart.clear()
        return redirect('orders:order_detail', order.id)  # Redirect to order detail view


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Orders
    template_name = 'order.html'
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_items = self.object.order_items.all()
        context['order_items'] = order_items
        return context


class UpdateStatusView(TemplateView):
    template_name = 'order.html'

    def post(self, request, *args, **kwargs):
        order_id = self.kwargs['order_id']
        order = get_object_or_404(Orders, id=order_id)
        order.status = True
        order.save()
        return redirect('api:profile', pk=order.customer.pk)


# class UserOrdersView(LoginRequiredMixin, ListView):
#     model = Orders
#     context_object_name = 'orders'
#     template_name = 'user_orders.html'
#
#     def get_queryset(self):
#         return self.request.user.orders.all()
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Orders'
#         return context



from django.shortcuts import render, get_object_or_404
from order.models import Orders


def order(request, id):
    order = get_object_or_404(Orders, pk=id)
    return render(request, "order.html", {"order": order})

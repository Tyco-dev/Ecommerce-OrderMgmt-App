from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Item


# Create your views here.


def home_view(request):
    context = {}
    return render(request, 'store/home-page.html', context)


class CatalogView(ListView):
    model = Item
    template_name = 'store/catalog.html'


class ItemDetailView(DetailView):
    model = Item
    template_name = 'store/product_detail.html'


def checkout_view(request):
    context = {}
    return render(request, 'store/checkout-page.html', context)


def product_detail_view(request):
    context = {}
    return render(request, 'store/product_detail.html', context)

from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.db.models import F
from django.contrib import messages
from .models import Item, Order, OrderItem
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.


def home_view(request):
    context = {}
    return render(request, 'store/home-page.html', context)


class CatalogView(ListView):
    model = Item
    paginate_by = 10
    template_name = 'store/catalog.html'


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'store/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("/")


class ItemDetailView(DetailView):
    model = Item
    template_name = 'store/product_detail.html'


def checkout_view(request):
    context = {}
    return render(request, 'store/checkout-page.html', context)


def product_detail_view(request):
    context = {}
    return render(request, 'store/product_detail.html', context)


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity = F('quantity') + 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("store:order_summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("store:catalog")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("store:order_summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("store:order_summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("store:product_detail", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("store:product_detail", slug=slug)



@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("store:order_summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("store:product_detail", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("store:product_detail", slug=slug)

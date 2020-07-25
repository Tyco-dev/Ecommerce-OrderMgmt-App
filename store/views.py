from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.db.models import F
from django.contrib import messages
from .models import Item, Order, OrderItem, BillingAddress, Payment
from django.core.exceptions import ObjectDoesNotExist
from .forms import CheckOutForm

# Create your views here.

import stripe
from stripe import error

stripe.api_key = settings.STRIPE_SECRET_KEY


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


class CheckOutView(View):
    def get(self, *args, **kwargs):
        # form
        form = CheckOutForm()
        context = {
            'form': form
        }
        return render(self.request, 'store/checkout-page.html', context)

    def post(self, *args, **kwargs):
        form = CheckOutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                phone = form.cleaned_data.get('phone_number')
                street_address = form.cleaned_data.get('street_address')
                suite_address = form.cleaned_data.get('suite_address')
                state = form.cleaned_data.get('state')
                zip = form.cleaned_data.get('zip')
                delivery_date = form.cleaned_data.get('delivery_date')
                # TODO: add functionality to these fields
                # same_shipping_address = form.cleaned_data.get('same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    phone_number=phone,
                    street_address=street_address,
                    suite_address=suite_address,
                    state=state,
                    zip=zip,
                )
                billing_address.save()
                order.delivery_date = delivery_date
                order.billing_address = billing_address
                order.save()

                if payment_option == 'S':
                    return redirect('store:payment', payment_option='stripe')
                elif payment_option == 'INV':
                    return redirect('store:payment', payment_option='invoice')
                else:
                    messages.warning(self.request, "Failed Checkout")
                    return redirect('store:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "Invalid payment option selected")
            return redirect("store:order_summary")


class PaymentView(View):
    def get(self, *args, **kwargs):
        # order
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'order': order
        }
        return render(self.request, "store/payment.html", context)

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total() * 100)  # cents

        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=token,
            )

            # create payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

            # assign the payment to order

            order.ordered = True
            order.payment = payment
            order.save()

            messages.success(self.request, "Your order was successful")
            return redirect("/")

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            messages.error(self.request, f"{err.get('message')}")
            return redirect("/")

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(self.request, "Rate limit error")
            return redirect("/")

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(self.request, "Invalid Request Error")
            return redirect("/")

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(self.request, "Authentication Error")
            return redirect("/")

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(self.request, "Network Error")
            return redirect("/")

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(self.request, "Something went wrong. You were not charged. Please try again")
            return redirect("/")

        except Exception as e:
            # send email to ourselves
            messages.error(self.request, "A serious error has occurred, please contact us")
            return redirect("/")


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

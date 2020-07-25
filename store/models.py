from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from localflavor.us.models import USStateField


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

MEASUREMENT_CHOICES = (
    ('OZ', 'ounce'),
    ('LB', 'pound'),
    ('FLOZ', 'fluid ounce')
)


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    weight = models.FloatField(blank=True, null=True)
    measurement = models.CharField(choices=MEASUREMENT_CHOICES, max_length=4, blank=True, null=True)
    description = models.CharField(max_length=500, default='Enter description for item')
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, blank=True, null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.DO_NOTHING, blank=True, null=True)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1, null=True, blank=True)
    featured = models.BooleanField(default=False)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("store:product_detail", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("store:add_to_cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("store:remove_from_cart", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    delivery_date = models.DateField(null=True)
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        # if self.coupon:
        #     total -= self.coupon.amount
        return total


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    street_address = models.CharField(max_length=100)
    suite_address = models.CharField(max_length=100)
    state = USStateField()
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
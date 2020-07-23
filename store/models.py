from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify

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

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Item, self).save(*args, **kwargs)


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

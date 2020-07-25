from django import template
from store.models import Order

register = template.Library()


@register.filter
def cart_item_count(user):
    # check if user is authenticated
    if user.is_authenticated:
        # get order query set, dont retrieve previous placed orders
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0

from django.urls import path
from .views import home_view, CatalogView, checkout_view, ItemDetailView, add_to_cart, remove_from_cart, OrderSummaryView, remove_single_item_from_cart

app_name = 'store'

urlpatterns = [
    path('', home_view, name='home'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('checkout/', checkout_view, name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order_summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product_detail'),
    path('add-to-cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove_single_item_from_cart'),
]

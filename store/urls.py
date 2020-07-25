from django.urls import path
from .views import home_view, CatalogView, ItemDetailView, add_to_cart, remove_from_cart, OrderSummaryView, remove_single_item_from_cart, CheckOutView, PaymentView

app_name = 'store'

urlpatterns = [
    path('', home_view, name='home'),
    path('checkout/', CheckOutView.as_view(), name='checkout'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('order-summary/', OrderSummaryView.as_view(), name='order_summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product_detail'),
    path('add-to-cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove_single_item_from_cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment')
]

from django.urls import path
from .views import home_view, CatalogView, checkout_view, ItemDetailView

app_name = 'store'

urlpatterns = [
    path('', home_view, name='home'),
    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('checkout/', checkout_view, name='checkout'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product_detail'),
]

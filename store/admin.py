from django.contrib import admin
from .models import Item, OrderItem, Order, Category, SubCategory, BillingAddress, Payment

# Register your models here.


admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(BillingAddress)
admin.site.register(Payment)


class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Item, ItemAdmin)

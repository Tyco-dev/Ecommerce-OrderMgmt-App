from django.contrib import admin
from .models import Item, OrderItem, Order, Category, SubCategory

# Register your models here.


admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(SubCategory)


class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Item, ItemAdmin)

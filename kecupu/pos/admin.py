from django.contrib import admin

# Add your admin site registrations here, eg.
from kecupu.pos.models import Customer, Store, Item, Order, OrderItem
from kecupu.pos.admin_utils import ButtonableModelAdmin

class CustomerAdmin(ButtonableModelAdmin):
    list_display = ('name', 'address')
    search_fields = ['name']

    def list_orders(self, request, obj):
        pass
    list_orders.short_description = 'Orders'
    buttons = [list_orders]

admin.site.register(Customer, CustomerAdmin)

class StoreAdmin(admin.ModelAdmin):
    pass
admin.site.register(Store, StoreAdmin)

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'store')
admin.site.register(Item, ItemAdmin)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'store', 'created')
    inlines = (OrderItemInline,)
    list_filter = ('customer',)
admin.site.register(Order, OrderAdmin)

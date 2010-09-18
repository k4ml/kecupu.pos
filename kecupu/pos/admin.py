from django.contrib import admin

# Add your admin site registrations here, eg.
from kecupu.pos.models import Customer, Store, Item

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ['name']
admin.site.register(Customer, CustomerAdmin)

class StoreAdmin(admin.ModelAdmin):
    pass

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'store')
admin.site.register(Item, ItemAdmin)

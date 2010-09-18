from django.contrib import admin

# Add your admin site registrations here, eg.
from kecupu.pos.models import Customer, Store

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ['name']
admin.site.register(Customer, CustomerAdmin)

class StoreAdmin(admin.ModelAdmin):
    pass
admin.site.register(Store, StoreAdmin)

from django.conf.urls.defaults import *

urlpatterns = patterns('kecupu.pos.views',
    (r'^$', 'index'),
    (r'^order/new$', 'new_order'),
    (r'^order/new/(\d+)$', 'current_order'),
    (r'^customer/autocomplete$', 'customer_autocomplete'),
    (r'^item/autocomplete$', 'item_autocomplete'),
)

from django.conf.urls.defaults import *

urlpatterns = patterns('kecupu.pos.views',
    (r'^$', 'index'),
    (r'^order/new$', 'new_order'),
    (r'^order/(\d+)$', 'current_order'),
    (r'^order/(\d+)/update$', 'update_order'),
    (r'^order/(\d+)/add-item$', 'add_order_item'),
    (r'^customer/autocomplete$', 'customer_autocomplete'),
    (r'^item/autocomplete$', 'item_autocomplete'),
)

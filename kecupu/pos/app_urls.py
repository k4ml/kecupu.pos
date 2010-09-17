from django.conf.urls.defaults import *

urlpatterns = patterns('kecupu.pos.views',
    (r'^$', 'index'),
    (r'^order/new$', 'new_order'),
)

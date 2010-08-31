from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

# URL patterns for kecupu.pos

urlpatterns = patterns('kecupu.pos.views',
  # Add url patterns here
  # TODO: This should include from kecupu.pos.app_urls
  (r'^$', 'index'),
  (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

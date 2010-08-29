from django.conf.urls.defaults import *
from django.conf import settings

# URL patterns for kecupu.pos

urlpatterns = patterns('kecupu.pos.views',
  # Add url patterns here
  (r'^$', 'index'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

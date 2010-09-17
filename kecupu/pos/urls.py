from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

# URL patterns for kecupu.pos

urlpatterns = patterns('',
  # Add url patterns here
  # TODO: This should include from kecupu.pos.app_urls
  (r'^', include('kecupu.pos.app_urls')),
)

urlpatterns += patterns('',
  (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('django.contrib.auth.views',
  (r'^accounts/login/$', 'login', {'template_name': 'kecupu.pos/login.html'}),
  (r'^accounts/logout/$', 'logout_then_login'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

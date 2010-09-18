from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

from django.contrib.auth.views import logout_then_login

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

def logout(request):
    try:
        del request.session['store_id']
    except:
        pass
    return logout_then_login(request)

urlpatterns += patterns('django.contrib.auth.views',
  (r'^accounts/login/$', 'login', {'template_name': 'kecupu.pos/login.html'}),
  url(r'^accounts/logout/$', logout, name="logout_then_login"),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

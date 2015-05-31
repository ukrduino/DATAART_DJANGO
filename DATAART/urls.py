import sys

from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^captcha/', include('captcha.urls')),
                       url(r'^', include('ITFORUM.urls')),

                       )


# comment on pythonanywhere
if not sys.platform.startswith('linux'):
    if settings.DEBUG:
        import debug_toolbar

        urlpatterns += patterns('',
                                url(r'^__debug__/', include(debug_toolbar.urls)),
                                )

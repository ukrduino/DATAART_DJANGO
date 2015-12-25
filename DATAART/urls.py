import sys

from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^captcha/', include('captcha.urls')),
                       url(r'^', include('IT_FORUM.urls')),
                       )

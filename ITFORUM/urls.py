from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'ITFORUM.views.start_page', name="home"),
                       )

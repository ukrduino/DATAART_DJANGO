from django.conf.urls import patterns, url

urlpatterns = patterns('ITFORUM.views',
                       url(r'^$', 'start_page', name="home"),
                       url(r'login', 'user_login', name='user_login'),
                       url(r'logout', 'user_logout', name='user_logout'),
                       )

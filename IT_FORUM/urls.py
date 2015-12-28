from django.conf.urls import url
from IT_FORUM.views import *

urlpatterns = [
    url(r'^$', show_home_page, name="home"),
    url(r'login$', user_login, name='user_login'),
    url(r'logout$', user_logout, name='user_logout'),
    url(r'threads_category/([0-9]+)$', threads_category_page,
        name='threads_category_page'),
    url(r'new_thread/$', new_thread, name='new_thread'),
    url(r'thread/([0-9]+)$', thread_page, name="thread_page"),
    url(r'thread/([0-9]+)#([0-9]+)$', thread_page, name="thread_page"),
    url(r'thread/([0-9]+)/([0-9]+)/([0-1])$', thread_page, name="thread_page"),
    url(r'new_reply/$', new_reply, name='new_reply'),
]

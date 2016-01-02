from django.conf.urls import url
from django.conf.urls.static import static
from DATAART import settings
from IT_FORUM.views import *

urlpatterns = [
    url(r'^$', show_home_page, name="home"),
    url(r'login$', user_login, name='user_login'),
    url(r'logout$', user_logout, name='user_logout'),
    url(r'register$', user_register, name='user_register'),
    url(r'threads_category/([0-9]+)/$', show_threads_page,
        name='threads_category_page'),
    url(r'new_thread/$', new_thread, name='new_thread'),
    url(r'thread/([0-9]+)/$', thread_page, name="thread_page"),
    url(r'new_reply/$', new_reply, name='new_reply'),
    url(r'set_reply_id/$', set_reply_id),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.db import models

from DATAART.settings import MEDIA_ROOT


class Category(models.Model):
    class Meta:
        db_table = 'category'
        verbose_name = 'Thread category'
        verbose_name_plural = 'Thread categories'

    category_title = models.CharField(max_length=250, verbose_name='Title', blank=False, unique=True)
    parent_category = models.ForeignKey("self", blank=True, null=True)

    def __str__(self):
        return self.category_title

    def __unicode__(self):
        return self.thread_title


class Thread(models.Model):
    class Meta:
        db_table = 'thread'
        verbose_name = 'Thread'
        verbose_name_plural = 'Threads'

    thread_author = models.CharField(max_length=250, verbose_name='Your name', blank=True)
    thread_author_email = models.EmailField(verbose_name='Your e-mail', blank=True)
    thread_title = models.CharField(max_length=250, verbose_name='Thread title', blank=False, unique=True)
    thread_text = models.TextField(verbose_name='Thread description', blank=False)
    thread_date = models.DateTimeField(auto_now_add=True, verbose_name='Created', blank=False)
    thread_change_date = models.DateTimeField(auto_now=True, verbose_name='Changed')
    thread_category = models.ForeignKey(Category)
    thread_image = models.ImageField(upload_to=MEDIA_ROOT, default="static/ImageNot.jpg")

    def __str__(self):
        return self.thread_title

    def __unicode__(self):
        return self.thread_title


class Reply(models.Model):
    class Meta:
        db_table = 'reply'
        verbose_name = 'Reply'
        verbose_name_plural = 'Replies'

    reply_author = models.CharField(max_length=250, verbose_name='Your name', blank=True)
    reply_author_email = models.EmailField(verbose_name='Your e-mail', blank=True)
    reply_text = models.TextField(verbose_name='Reply text', blank=False)
    reply_date = models.DateTimeField(auto_now_add=True, verbose_name='Created', blank=False)
    reply_to_thread = models.ForeignKey(Thread, null=True)
    reply_to_reply = models.ForeignKey("self", blank=True, null=True, related_name='replies_to_this')

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)

from django.contrib.auth import backends, get_user_model
from django.db.models import Q


class ModelBackend(backends.ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))

            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password)
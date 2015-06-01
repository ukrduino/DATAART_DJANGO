from django.core.files.storage import FileSystemStorage
from django.db import models

fs = FileSystemStorage(location='/media')

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

    thread_title = models.CharField(max_length=250, verbose_name='Thread title', blank=False, unique=True)
    thread_text = models.TextField(verbose_name='Thread description', blank=False)
    thread_date = models.DateTimeField(auto_now_add=True, verbose_name='Created', blank=False)
    thread_change_date = models.DateTimeField(auto_now=True, verbose_name='Changed')
    thread_category = models.ForeignKey(Category)
    thread_image = models.ImageField(fs, null=True, blank=True)

    def __str__(self):
        return self.thread_title

    def __unicode__(self):
        return self.thread_title


class Reply(models.Model):
    class Meta:
        db_table = 'reply'
        verbose_name = 'Reply'
        verbose_name_plural = 'Replies'

    reply_text = models.TextField(verbose_name='Reply text', blank=False)
    reply_date = models.DateTimeField(auto_now_add=True, verbose_name='Created', blank=False)
    reply_to_thread = models.ForeignKey(Thread)
    reply_to_reply = models.ForeignKey("self", blank=True, null=True)

    def __str__(self):
        return self.pk

    def __unicode__(self):
        return self.pk

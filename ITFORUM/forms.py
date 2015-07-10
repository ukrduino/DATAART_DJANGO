from django.forms import ModelForm
from ITFORUM.models import Thread, Reply


class ThreadForm(ModelForm):

    class Meta:
        model = Thread
        exclude = ["pk", 'thread_category']


class ReplyForm(ModelForm):

    class Meta:
        model = Reply
        exclude = ["pk", 'reply_to_thread', 'reply_to_reply']

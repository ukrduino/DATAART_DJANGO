
from django.forms import ModelForm, ModelChoiceField
from IT_FORUM.models import Thread, Reply


class ThreadForm(ModelForm):

    class Meta:
        model = Thread
        exclude = ["pk", 'thread_category']


class ReplyForm(ModelForm):

    class Meta:
        model = Reply
        thread = ModelChoiceField(queryset=Thread.objects.all())
        exclude = ["pk", 'reply_to_thread', 'reply_to_reply']

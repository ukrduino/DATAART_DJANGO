from django.forms import ModelForm
from ITFORUM.models import Thread, Category


class ThreadForm(ModelForm):

    class Meta:
        model = Thread
        exclude = ["pk", 'thread_category']

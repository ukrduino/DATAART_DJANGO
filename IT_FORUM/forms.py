from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from IT_FORUM.models import Thread, Reply


class ThreadForm(ModelForm):

    class Meta:
        model = Thread
        exclude = ["pk", 'thread_category']


class ReplyForm(ModelForm):

    class Meta:
        model = Reply
        exclude = ['reply_to_thread', 'reply_to_reply']


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

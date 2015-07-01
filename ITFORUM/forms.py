from django.forms import ModelForm
from ITFORUM.models import Thread, Category


class ThreadForm(ModelForm):

    def __init__(self, category, *args, **kwargs):
            super(ThreadForm, self).__init__(*args, **kwargs)
            self.fields['thread_category'].queryset = Category.objects.filter(parent_category__category_title=category)

    class Meta:
        model = Thread
        exclude = ["pk"]


# http://stackoverflow.com/questions/291945/how-do-i-filter-foreignkey-choices-in-a-django-modelform
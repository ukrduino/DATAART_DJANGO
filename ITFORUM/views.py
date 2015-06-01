from django.shortcuts import render_to_response

# Create your views here.
from django.template import RequestContext
from ITFORUM.models import Category


def start_page(request):
    args = dict()
    args['Hobbies'] = Category.objects.get(category_title="Hobbies")
    args['HiTech'] = Category.objects.get(category_title="Hi-Tech")
    args['Talks'] = Category.objects.get(category_title="Talks")
    args['BigBoss'] = Category.objects.get(category_title="Big Boss")
    args['HR'] = Category.objects.get(category_title="HR")
    args['Hobbies_categories'] = Category.objects.filter(parent_category__category_title="Hobbies")
    args['HiTech_categories'] = Category.objects.filter(parent_category__category_title="Hi-Tech")
    args['Talks_categories'] = Category.objects.filter(parent_category__category_title="Talks")
    args['BigBoss_categories'] = Category.objects.filter(parent_category__category_title="Big Boss")
    args['HR_categories'] = Category.objects.filter(parent_category__category_title="HR")
    # args['main_categories'] = Category.objects.all()
    return render_to_response("StartPage.html", args, context_instance=RequestContext(request))

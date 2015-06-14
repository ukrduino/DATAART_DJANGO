from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, render

# Create your views here.
from django.template import RequestContext
from ITFORUM.models import Category, Thread, ThreadForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


def start_page(request):
    args = dict()
    args['Hobbies'] = Category.objects.get(category_title="Hobbies")
    args['HiTech'] = Category.objects.get(category_title="Hi-Tech")
    args['Talks'] = Category.objects.get(category_title="Talks")
    args['BigBoss'] = Category.objects.get(category_title="Big Boss")
    args['HR'] = Category.objects.get(category_title="HR")
    if request.user.is_authenticated():
        args['BigBoss_categories'] = Category.objects.filter(parent_category__category_title="Big Boss")
        args['HR_categories'] = Category.objects.filter(parent_category__category_title="HR")
    args['Hobbies_categories'] = Category.objects.filter(parent_category__category_title="Hobbies")
    args['HiTech_categories'] = Category.objects.filter(parent_category__category_title="Hi-Tech")
    args['Talks_categories'] = Category.objects.filter(parent_category__category_title="Talks")
    return render_to_response("BoardPageContent.html", args, context_instance=RequestContext(request))

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    return HttpResponse("Inactive User")
            else:
                return HttpResponse("Bad Job")
    else:
        form = AuthenticationForm()
    return render(request, 'LoginPage.html', {
        'form': form,
    })

def user_logout(request):
    logout(request)
    return redirect('/')

def threads_page(request):
    args = dict()
    args["form"] = ThreadForm()
    categories_with_subcategories = dict()
    main_cats = Category.objects.filter(parent_category=None)
    # print(main_cats)
    for main_cat in main_cats:
        categories_with_subcategories[main_cat.category_title] = Category\
            .objects.filter(parent_category__category_title=main_cat.category_title)
        # for i in categories_with_subcategories[main_cat.category_title]:
        #     print(i)
    if request.user.is_anonymous():
        del categories_with_subcategories["HR"]
        del categories_with_subcategories["Big Boss"]
    args['main_categories'] = categories_with_subcategories
    return render_to_response("ThreadsPageContent.html", args, context_instance=RequestContext(request))

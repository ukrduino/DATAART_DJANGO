from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, render

from django.template import RequestContext
from ITFORUM.forms import ThreadForm
from ITFORUM.models import Category, Thread, Reply
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


def start_page(request):
    args = dict()
    categories_with_subcategories = dict()
    main_cats = Category.objects.filter(parent_category=None)
    for main_cat in main_cats:
        categories_with_subcategories[main_cat.category_title] = Category\
            .objects.filter(parent_category__category_title=main_cat.category_title)
    if request.user.is_anonymous():
        del categories_with_subcategories["HR"]
        del categories_with_subcategories["Big Boss"]
    args['main_categories'] = categories_with_subcategories
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

def threads_category_page(request, category_id=6):
    args = dict()
    args["form"] = ThreadForm()
    categories_with_subcategories = dict()
    main_cats = Category.objects.filter(parent_category=None)
    for main_cat in main_cats:
        categories_with_subcategories[main_cat.category_title] = Category\
            .objects.filter(parent_category__category_title=main_cat.category_title)
    if request.user.is_anonymous():
        del categories_with_subcategories["HR"]
        del categories_with_subcategories["Big Boss"]
    args['main_categories'] = categories_with_subcategories
    args['threads'] = Thread.objects.filter(thread_category__id=category_id)
    args['category'] = Category.objects.get(id=category_id)
    args['category_id'] = category_id
    return render_to_response("ThreadsPageContent.html", args, context_instance=RequestContext(request))

def new_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        category = Category.objects.get(id=request.context.get('category_id'))
        print(request.session.get('category_id'))
        if form.is_valid():
            add_thread = form.save(commit=False)
            add_thread.thread_category = category
            add_thread.save()
        else:
            form = ThreadForm()

    # http://stackoverflow.com/a/12758859/3177550
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def thread_page(request, thread_id=1):
    args = dict()
    args["form"] = ThreadForm()
    categories_with_subcategories = dict()
    main_cats = Category.objects.filter(parent_category=None)
    for main_cat in main_cats:
        categories_with_subcategories[main_cat.category_title] = Category\
            .objects.filter(parent_category__category_title=main_cat.category_title)
    if request.user.is_anonymous():
        del categories_with_subcategories["HR"]
        del categories_with_subcategories["Big Boss"]
    args['main_categories'] = categories_with_subcategories
    args['thread'] = Thread.objects.get(id=thread_id)
    args['replies'] = Reply.objects.filter(reply_to_thread__id=thread_id)
    return render_to_response("ThreadPageContent.html", args, context_instance=RequestContext(request))


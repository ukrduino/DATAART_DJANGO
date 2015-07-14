from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
from ITFORUM.forms import ThreadForm, ReplyForm
from ITFORUM.models import Category, Thread, Reply
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

def categories_for_header(request):
    categories_with_subcategories = dict()
    main_cats = Category.objects.filter(parent_category=None)
    for main_cat in main_cats:
        categories_with_subcategories[main_cat.category_title] = Category\
            .objects.filter(parent_category__category_title=main_cat.category_title)
    if request.user.is_anonymous():
        del categories_with_subcategories["HR"]
        del categories_with_subcategories["Big Boss"]
    return categories_with_subcategories

def start_page(request):
    args = dict()
    args['main_categories'] = categories_for_header(request)
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
    args['main_categories'] = categories_for_header(request)
    # for form
    args["form"] = ThreadForm
    request.session['category_id'] = category_id
    request.session['category_title'] = Category.objects.get(id=category_id).category_title
    # for threads
    threads_with_comments = dict()
    threads = Thread.objects.filter(thread_category__id=category_id)
    for thread in threads:
        reversed_comments_list = list(reversed(Reply.objects.filter(reply_to_thread__id=thread.id)))
        threads_with_comments[thread] = reversed_comments_list[:2]
    args['threads_with_comments'] = threads_with_comments
    return render_to_response("ThreadsPageContent.html", args, context_instance=RequestContext(request))

def new_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            add = form.save(commit=False)
            add.thread_category_id = request.session['category_id']
            add.save()

    # http://stackoverflow.com/a/12758859/3177550
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def thread_page(request, thread_id=1, reply_id=0, form=0):
    args = dict()
    args['main_categories'] = categories_for_header(request)
    request.session['thread_id'] = thread_id
    if form:
        args["form"] = ReplyForm
    if reply_id:
        request.session['reply_id'] = reply_id
    args['thread'] = Thread.objects.get(id=thread_id)
    args['replies'] = list(reversed(Reply.objects.filter(reply_to_thread__id=thread_id)))
    return render_to_response("ThreadPageContent.html", args, context_instance=RequestContext(request))

def new_reply(request):
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            add = form.save(commit=False)
            add.reply_to_thready_id = int(request.session['thread_id'])
            if request.session['reply_id']:
                add.reply_to_reply_id = request.session['reply_id']
            add.save()

    # http://stackoverflow.com/a/12758859/3177550
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


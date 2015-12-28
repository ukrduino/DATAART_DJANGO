from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from IT_FORUM.forms import ThreadForm, ReplyForm
from IT_FORUM.models import Category, Thread, Reply
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


def get_categories_and_subcategories(request):
    categories_with_subcategories_dict = dict()
    categories_with_subcategories_dict["Hobbies"] = Category.objects.filter(
        parent_category__category_title="Hobbies")
    categories_with_subcategories_dict["Hi_Tech"] = Category.objects.filter(
        parent_category__category_title="Hi-Tech")
    categories_with_subcategories_dict["Talks"] = Category.objects.filter(
        parent_category__category_title="Talks")
    if request.user.is_authenticated():
        categories_with_subcategories_dict["Big_Boss"] = Category.objects\
            .filter(parent_category__category_title="Big Boss")
        categories_with_subcategories_dict["HR"] = Category.objects.filter(
            parent_category__category_title="HR")
    return categories_with_subcategories_dict


def replies_for_thread(request):
    replies_with_replies = dict()
    base_replies = Reply.objects.filter(reply_to_reply=None)
    for reply in base_replies:
        replies_with_replies[reply.id] = Reply.objects.filter(
            reply_to_reply__id=reply.id)
    return replies_with_replies


def show_home_page(request):
    args = dict()
    args['main_categories'] = get_categories_and_subcategories(request)
    return render(request, "Dashboard_page_content.html", args)


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
    args['main_categories'] = get_categories_and_subcategories(request)
    # for form
    args["form"] = ThreadForm
    request.session['category_id'] = category_id
    request.session['category_title'] = Category.objects.get(id=category_id)\
        .category_title
    # for threads
    threads_with_replies = dict()
    threads = Thread.objects.filter(thread_category__id=category_id)
    for thread in threads:
        reversed_comments_list = list(reversed(Reply.objects.filter(
            reply_to_thread__id=thread.id)))
        threads_with_replies[thread] = reversed_comments_list[:2]
    args['threads_with_replies'] = threads_with_replies
    return render(request, "Threads_page_content.html", args)


def new_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            add = form.save(commit=False)
            add.thread_category_id = request.session['category_id']
            add.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def thread_page(request, thread_id=1, reply_id=0, form=0):
    args = dict()
    args['main_categories'] = get_categories_and_subcategories(request)
    args['replies'] = list(Reply.objects.filter(reply_to_thread__id=thread_id))
    # args['replies'] = replies_for_thread(request, thread_id)
    request.session['thread_id'] = thread_id
    if form:
        args["form"] = ReplyForm
        if reply_id:
            request.session['reply_id'] = reply_id
    args['thread'] = Thread.objects.get(id=thread_id)
    return render(request, "One_thread_content.html", args)


def new_reply(request):
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            add = form.save(commit=False)
            add.reply_to_thread_id = request.session['thread_id']
            if request.session['reply_id']:
                add.reply_to_reply_id = request.session['reply_id']
            add.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

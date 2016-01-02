from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from IT_FORUM.forms import ThreadForm, ReplyForm, UserCreateForm
from IT_FORUM.models import Category, Thread, Reply
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


def get_cat_and_subcat_dict(request):
    categories_with_subcategories_dict = dict()
    categories_with_subcategories_dict["Hobbies"] = Category.objects.filter(
        parent_category__category_title="Hobbies")
    categories_with_subcategories_dict["Hi_Tech"] = Category.objects.filter(
        parent_category__category_title="Hi-Tech")
    categories_with_subcategories_dict["Talks"] = Category.objects.filter(
        parent_category__category_title="Talks")

    # User should be authenticated to see these categories
    if request.user.is_authenticated():
        categories_with_subcategories_dict["Big_Boss"] = Category.objects\
            .filter(parent_category__category_title="Big Boss")
        categories_with_subcategories_dict["HR"] = Category.objects.filter(
            parent_category__category_title="HR")
    return categories_with_subcategories_dict


def show_home_page(request):
    args = dict()
    args['main_categories'] = get_cat_and_subcat_dict(request)
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


def user_register(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            # save the new user first
            form.save()
            # get the username and password
            username = request.POST['username']
            password = request.POST['password1']
            # authenticate user then login
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = UserCreateForm()
    return render(request, 'RegistrationPage.html', {
        'form': form,
    })


def show_threads_page(request, category_id=6):
    args = dict()
    args['main_categories'] = get_cat_and_subcat_dict(request)
    args['threads_category_tittle'] = Category.objects.get(id=category_id)\
        .category_title
    # category_id will be used in processing of new thread form to create
    # new thread in certain category
    args["form"] = ThreadForm
    request.session['category_id'] = category_id
    threads_with_replies_dict = dict()
    threads = Thread.objects.filter(thread_category__id=category_id)
    for thread in threads:
        # for each thread we get two last replies
        replies_list = list(Reply.objects.filter(reply_to_thread__id=thread.id))[-2:]
        reply_with_sub_replies_dict = dict()
        for reply in replies_list:
            # for each reply we get sub replies
            sub_replies = Reply.objects.filter(reply_to_reply__id=reply.id)
            reply_with_sub_replies_dict[reply] = sub_replies
        threads_with_replies_dict[thread] = reply_with_sub_replies_dict
    args['threads_with_replies'] = threads_with_replies_dict
    return render(request, "Threads_page_content.html", args)


def new_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST, request.FILES)
        if form.is_valid():
            add = form.save(commit=False)
            add.thread_category_id = request.session['category_id']
            add.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def thread_page(request, thread_id=1):
    args = dict()
    args['main_categories'] = get_cat_and_subcat_dict(request)
    args['replies'] = list(Reply.objects.filter(reply_to_thread__id=thread_id))
    request.session['thread_id'] = thread_id
    args["form"] = ReplyForm
    args['thread'] = Thread.objects.get(id=thread_id)
    return render(request, "One_thread_content.html", args)


def set_reply_id(request):
    request.session['reply_id'] = request.POST['reply_id']
    return HttpResponse("reply_id was set")


def new_reply(request):
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            add = form.save(commit=False)
            add.reply_to_thread_id = request.session['thread_id']
            try:
                if request.session['reply_id']:
                    add.reply_to_reply_id = request.session['reply_id']
                    request.session['reply_id'] = 0
            except KeyError:
                pass
            finally:
                add.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, render

# Create your views here.
from django.template import RequestContext
from ITFORUM.models import Category
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
    return render_to_response("StartPage.html", args, context_instance=RequestContext(request))

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


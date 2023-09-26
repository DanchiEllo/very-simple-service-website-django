from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from worker.forms import UserRegistrationForm, UserAuthorizationForm
from worker.models import CustomUser
import datetime


def photo(request):
    return render(request, 'pages/test_photo.html')

def my_profile(request):
    user_profile = request.user
    return render(request,"users/my_profile.html", {'user_prof' : user_profile})

def profile(request,pk):
    user = get_user_model()
    user_profile = user.objects.get(pk = pk)

    return render(request,"users/profile.html", {'user_prof' : user_profile})
# Create your views here.

def userlist(request):
    list_user = CustomUser.objects.all()
    return render(request,'users/all_profiles.html',{'list_user':list_user})

def logout_site(request):
    logout(request)
    return HttpResponseRedirect('/')

def home(request):
    executors = CustomUser.objects.filter(groups__name='Исполнитель')
    customers = CustomUser.objects.filter(groups__name='Заказчик')
    list_user = CustomUser.objects.all()
    return render(request, 'pages/base.html', {'executors':executors, 'customers': customers, 'list_user': list_user})

def RegistrationForm(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserRegistrationForm(request.POST, request.FILES or None)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']

            user = authenticate(username=username, password=password)
            if user and user.is_active:
                login(request, user)
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserRegistrationForm()

    return render(request, 'users/registration.html', {'form': form})

def AuthorizationForm(request):
    if request.method == 'POST':
        form = UserAuthorizationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                form.add_error(None, 'Неверный логин или пароль')
                return render(request, 'users/authorization.html', {'form': form})
        else:
            return render(request, 'users/authorization.html', {'form': form})
    else:
        return render(request, 'users/authorization.html', {'form': UserAuthorizationForm()})
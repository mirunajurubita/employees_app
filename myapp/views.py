import datetime
from multiprocessing.dummy import Manager
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect 
from django.urls import reverse
from .models import User, Tasks
from .forms import LoginForm
#from myapp.EmailBackEnd import EmailBackEnd

from django.utils import timezone


def index(request):
    return render(request,"index.html")


def loginUser(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            #or user.is_superuser
            if user is not None and (user.is_admin):
                login(request, user)
                return HttpResponseRedirect(reverse('managerPage'))
            elif user is not None and user.is_employee:
                login(request, user)

                return HttpResponseRedirect(reverse('employeePage'))
            elif user is not None and user.is_superuser:
                login(request, user)

                return HttpResponseRedirect(reverse('adminPage'))
            else:
                msg= 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'index.html', {'form': form})


def logoutUser(request):
    logout(request)
    return redirect("/")
    #return HttpResponseRedirect("/")


def adminPage(request):
    return render(request, "admin_page.html")
"""
def resetPassword(request):

    return render(request, 'reset_password_page.html')
    """
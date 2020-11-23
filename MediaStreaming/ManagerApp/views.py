from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . import forms,models
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import psutil


def loginPage(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        # print(form)
        if form.is_valid():
            username = request.POST.get('username',"")
            password = request.POST.get('password',"")
            user = authenticate(request,username =username,password=password)
            if user is not None:
                login(request,user)
                return redirect("ManagerApp:dashboard")
            else:
                messages.error(request, 'Invalid Credintails')
                print("User  Error")


    form = forms.LoginForm(initial={'remember_me': False})
    context = {'title': "Manager App", 'form': form}
    return render(request,
    'ManagerApp/index.html',context)


def logoutUser(request):
    logout(request)
    return redirect("ManagerApp:loginPage")
    
@login_required(login_url="ManagerApp:loginPage")
def dashboard(request):
    movies = models.Movies.objects.count()



    context={'title': "Manager App - Dashborad",
        "total_movies":movies,
        "total_series":0,
        "pending_requests":0,
        "server_load":psutil.cpu_percent(),
        "cpu_usage":psutil.cpu_percent(),
        "ram_usage":psutil.virtual_memory().percent,
        "active_nav_item":"movies",
        "active_nav_item":"dashboard"}

    return render(request,'ManagerApp/dashboard.html',context)

import requests
def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def test(request):
    movie = models.Movies.objects.get(id=5)
    form = forms.FirebaseCredentialsForm()
    context = {
        "form":form
    }
    return render(request,'ManagerApp/test/test.html',context)

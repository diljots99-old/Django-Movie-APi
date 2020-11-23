from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . import forms ,models,database

from .external_apis import Tmdb_api

import datetime

from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

from django.contrib import messages

from django.core.paginator import Paginator


@login_required(login_url="ManagerApp:loginPage")
def manage_sources_movies(request):
    items_per_page = request.POST.get("items_per_page",25)
    page_number = request.GET.get("page",1)


    credentials = models.FirebaseCredentials.objects.all()
    pages = Paginator(credentials,items_per_page)
   

    context={'title': "Manager App - Movies - Manage Sources",
        "pages":pages,
        "page_obj":pages.get_page(page_number),
        "current_page_no":page_number,
        "active_nav_item":"movies",
        "sub_menu_item":[False,True,False,False]}
    return render(request,'ManagerApp/movies/manage_source.html',context)

@login_required(login_url="ManagerApp:loginPage")
def add_new_firebase_credentials(request):
    import json
    form = forms.FirebaseCredentialsForm()

    if request.method =="POST":
        form = forms.FirebaseCredentialsForm(request.POST)
        
        if form.is_valid():
            try:
                serviceAccount = request.POST.get('serviceAccount',"")
                owner_email = request.POST.get('owner_email',"")

                serviceAccount = json.loads(serviceAccount)
                serviceAccount["owner_email"] = owner_email
                credentials = models.FirebaseCredentials(**serviceAccount)
                credentials.save()
                messages.success(request, 'credentials Added Succefully')
                
                return redirect("ManagerApp:manage_sources_movies")
            except Exception as e:
                messages.error(request, 'Error'+e)



    context={'title': "Manager App - Movies - Manage Sources",
    "form":form,
    "active_nav_item":"movies",
    "sub_menu_item":[False,True,False,False]}
    return render(request,'ManagerApp/firebase/add_new_firebase_credentials.html',context)

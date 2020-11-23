from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . import forms ,models,database

from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.contrib import messages


@login_required(login_url="ManagerApp:loginPage")
def upload_media_firebase(request,media_id):
    Type = request.GET.get("type","")

    movie = models.Movies.objects.get(id=media_id)

    form = forms.FirebaseMoviesForm(initial={"movie":movie})


    if request.method == 'POST':
        form = forms.FirebaseMoviesForm(request.POST)
        # print(form)
        if form.is_valid():
            try:
                
                form.save()

                if not movie.streamable:
                    movie.streamable =True
                    movie.save()
                messages.success(request, 'Media Upload Deatils Added Succesfully')
                
                
                return redirect("ManagerApp:movie_details",movie_id=media_id)
            except Exception as e:
                print(e)
                messages.warning(request, str(e))


    context={'title': "Manager App - Dashborad",
        "movie":model_to_dict(movie),
        "form":form,
        "active_nav_item":"movies",
        "sub_menu_item":[False,False,False,False]}

    return render(request,'ManagerApp/media/upload_media_firebase.html',context)


@login_required(login_url="ManagerApp:loginPage")
def upload_media_page(request,media_id):
    Type = request.GET.get("type","")

    movie = models.Movies.objects.get(id=media_id)

    form = forms.GoogleDriveSourceForm(initial={'backref_id': media_id,"type":Type})


    if request.method == 'POST':
        form = forms.GoogleDriveSourceForm(request.POST)
        # print(form)
        if form.is_valid():
            try:
                
                form.save()

                if not movie.streamable:
                    movie.streamable =True
                messages.success(request, 'Media Saved Succesfully')
                
                
                return redirect("ManagerApp:movie_details",movie_id=media_id)
            except Exception as e:
                print(e)
                messages.warning(request, str(e))







    context={'title': "Manager App - Dashborad",
        "movie":model_to_dict(movie),
        "form":form,
        "active_nav_item":"movies",
        "sub_menu_item":[False,False,False,False]}

    return render(request,'ManagerApp/media/uploadmedia.html',context)
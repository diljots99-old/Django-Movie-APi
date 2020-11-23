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

import psutil 

@login_required(login_url="ManagerApp:loginPage")
def movie_dashboard(request):
    movies = models.Movies.objects.count()

    movies = models.Movies.objects.order_by("-release_date").all()
    listOfmovies = []
    for movie in movies:
        listOfmovies.append(model_to_dict(movie))
        if len(listOfmovies) >= 70:
            break


    context={'title': "Manager App - Dashborad",
        "movies":listOfmovies,
        "total_movies":0,
        "total_series":0,
        "pending_requests":0,
        "server_load":psutil.cpu_percent(),
        "cpu_usage":psutil.cpu_percent(),
        "ram_usage":psutil.virtual_memory().percent,
        "active_nav_item":"movies",
        "sub_menu_item":[True,False,False,False]}
    return render(request,'ManagerApp/movie_dashboard.html',context)


@login_required(login_url="ManagerApp:loginPage")
def movie_details_page(request,movie_id):
    movie = models.Movies.objects.get(id=movie_id)
    movie = model_to_dict(movie)
    genres = database.Database().get_movie_genres(movie.get("id"))
    
    listGenres = []
    for genre in genres:
        listGenres.append(genre.get("name"))

    movie['genres'] = ','.join(listGenres)

    context={'title': "Manager App - Dashborad",
        "movie":movie,
       
        "active_nav_item":"movies",
        "sub_menu_item":[True,False,False,False]}

    return render(request,'ManagerApp/movie_details.html',context)





@login_required(login_url="ManagerApp:loginPage")
def add_new_movie(request):
    

    JSON = None
    search_query = None
    page_range = None
    
    if request.method == "POST":
        search_query = request.POST.get("search_query",None)
        if not search_query:
            search_query = request.GET.get("search_query",None)
        page  = request.GET.get("page",1)
        if isinstance(page,str):
            page = int(page)
        print(search_query)
        result , JSON = Tmdb_api().search_movie(query=search_query,language="en-US",page=page,include_adult=None,region=None,year=None,primary_release_year=None)
        
        for i in range(6):
            new_page = page + i
            if new_page == JSON.get('total_pages'):
                break
        page_range = range(page,new_page)
        if page == JSON.get('total_pages'):
            start = page-4
            end = page+1
            if start < 1:
                start = 1
            page_range = range(start,end)
        

    context={'title': "Manager App - Add New Movie",
    "active_nav_item":"movies",
    "search_results":JSON,
    "search_query":search_query,
    "page_range":page_range,
    "request":request,
    "sub_menu_item":[False,False,False,False]}
    return render(request,'ManagerApp/movies/add_new_movie.html',context)



@login_required(login_url="ManagerApp:loginPage")
def view_tmdb_result(request,movie_id):
    ID =movie_id

    JSON = Tmdb_api().get_movie_from_id(ID)




    context={'title': "Manager App - Add New Movie",
    "active_nav_item":"movies",
    "request":request,
    "movie":JSON,
    "sub_menu_item":[False,False,False,False]}
    return render(request,'ManagerApp/movies/view_tmdb_result.html',context)

@login_required(login_url="ManagerApp:loginPage")
def add_movie_to_system(request,movie_id):

    try:
        JSON = Tmdb_api().get_movie_from_id(movie_id)

        if models.Movies.objects.filter(id=movie_id).exists():
            movie = models.Movies.objects.get(id=movie_id)
            messages.warning(request, 'Movie Already in system. If You want to change try editing it')
            return redirect("ManagerApp:view_tmdb_result",movie_id = movie_id)

        else:
            if JSON.get("release_date") == "":
                JSON['release_date'] = None
            movie_data = {
                "adult" : JSON.get("adult"), 
                "id" : JSON.get("id"), 
                "imdb_id" : JSON.get("imdb_id",""), 
                "original_language" : JSON.get("original_language",""), 
                "original_title" : JSON.get("original_title",""), 
                "overview" : JSON.get("overview",""), 
                "release_date" : JSON.get("release_date",None), 
                "runtime" : JSON.get("runtime",""), 
                "status" : JSON.get("status",""), 
                "title" : JSON.get("title",""), 
                "tagline" : JSON.get("tagline",""), 
                "date_created" : datetime.datetime.today().strftime('%Y-%m-%d'), 
                "date_updated" : datetime.datetime.today().strftime('%Y-%m-%d'), 
                "streamable" : False, 
                "torrent" : False, 
                "vote_average" : JSON.get("vote_average",0), 
                "vote_count" : JSON.get("vote_count",0), 
                "popularity" : JSON.get("popularity",0) 
            }
            movie = models.Movies(**movie_data)
            movie.save()

        for genreJSON in JSON.get('genres'):
            if models.Genres.objects.filter(id=genreJSON.get("id")).exists():
                genre = models.Genres.objects.get(id=genreJSON.get("id"))
            else:
                genre = models.Genres(**genreJSON)
                genre.save()
            
            movieToGenres = models.MoviesToGenres(genre=genre,movie=movie)
            movieToGenres.save()

        for production_companies_JSON in JSON.get('production_companies'):
            if models.Companies.objects.filter(id=production_companies_JSON.get("id")).exists():
                company = models.Companies.objects.get(id=production_companies_JSON.get("id"))
            else:
                companyJSON = Tmdb_api().get_company_from_id(production_companies_JSON.get("id"))
                company_args = {
                    "id" : companyJSON.get("id"), 
                    "description" : companyJSON.get("description",""),
                    "headquarters" : companyJSON.get("headquarters",""),
                    "name" : companyJSON.get("name",""), 
                    "origin_country" : companyJSON.get("origin_country",""), 
                    "parent_company" : companyJSON.get("parent_company",""), 
                    "logo" : Tmdb_api().get_image(companyJSON.get("logo_path")), 
                    "homepage" : companyJSON.get("homepage",""), 

                }
                company = models.Companies(**company_args)
                company.save()

            moviesProductionCompanies = models.MoviesProductionCompanies(movie=movie,company=company)
            moviesProductionCompanies.save()
            messages.success(request, 'Movie Saved Succesfully')
        
    except Exception as e:
        messages.error(request, 'error while saving movie')


        
    return redirect("ManagerApp:view_tmdb_result",movie_id = movie_id)
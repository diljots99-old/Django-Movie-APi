from rest_framework.views import APIView
from rest_framework.response import Response

from .external_apis import Tmdb_api
from .database import Database
from .models import Movies
from .sources import MovieSources
from .views import SYSTEM_PEOPLE_ID,SYSTEM_MOVIE_ID
from django.http import HttpResponse
import io
from PIL import  Image

from rest_framework import status
from django.urls import reverse,reverse_lazy

from datetime import  date,timedelta
from django.contrib.sites.shortcuts import get_current_site

from django.forms.models import model_to_dict
from django.core.paginator import * 

from .app_settings  import SERVER_NAME


class get_now_playing_movies(APIView):
    def get(self,request,format=None):
        try:
            no_of_pages = request.GET.get("no_of_pages",None)
            page_no = request.GET.get("page_no",None)
            region = request.GET.get("region",None)

            try:
                if not no_of_pages is None:
                    no_of_pages = int(no_of_pages)
                if  not page_no is None:
                    page_no = int(page_no)
                if not region is None:
                    region = str(region)
            except Exception as e :
                print(e)

            api = Tmdb_api()
            myDb = Database() 
            listOfMovies = []
            for movieJson in  api.get_now_playing_movies(no_of_pages,page_no,region):
                ID = movieJson.get("id")
                movie = myDb.get_movies_from_id(ID = ID)

               
                if movie is not None:
                    listOfMovies.append(movie)

            return Response({"length":len(listOfMovies),"results":listOfMovies})

        except Exception as e: 
          return Response({ "message":"Exception Occured error",
                "exception_class": str(e.__class__),} )

class get_popular_movies(APIView):
    def get(self,request,format=None):
        try:
            no_of_pages = request.GET.get("no_of_pages",None)
            page_no = request.GET.get("page_no",None)
            region = request.GET.get("region",None)

            try:
                if not no_of_pages is None:
                    no_of_pages = int(no_of_pages)
                if  not page_no is None:
                    page_no = int(page_no)
                if not region is None:
                    region = str(region)
            except Exception as e :
                print(e)

            api = Tmdb_api()
            myDb = Database() 
            listOfMovies = []
            for movieJson in  api.get_popular_movies(no_of_pages,page_no,region):
                ID = movieJson.get("id")
                movie = myDb.get_movies_from_id(ID = ID)

               
                if movie is not None:
                    listOfMovies.append(movie)

            return Response({"length":len(listOfMovies),"results":listOfMovies})

        except Exception as e: 
            
            return Response({ "message":"Exception Occured error",
                "exception_class": str(e.__class__),} ,status=status.HTTP_400_BAD_REQUEST)

class get_top_rated_movies(APIView):
    def get(self,request,format=None):
        try:
            no_of_pages = request.GET.get("no_of_pages",None)
            page_no = request.GET.get("page_no",None)
            region = request.GET.get("region",None)

            try:
                if not no_of_pages is None:
                    no_of_pages = int(no_of_pages)
                if  not page_no is None:
                    page_no = int(page_no)
                if not region is None:
                    region = str(region)
            except Exception as e :
                print(e)

            api = Tmdb_api()
            myDb = Database() 
            listOfMovies = []
            for movieJson in  api.get_top_rated_movies(no_of_pages,page_no,region):
                ID = movieJson.get("id")
                movie = myDb.get_movies_from_id(ID = ID)

               
                if movie is not None:
                    listOfMovies.append(movie)

            return Response({"length":len(listOfMovies),"results":listOfMovies})

        except Exception as e: 
            
            return Response({ "message":"Exception Occured error",
                "exception_class": str(e.__class__),},status=status.HTTP_400_BAD_REQUEST)

class get_new_releases(APIView):
    def get(self,request,format=None):
        try:
            no_of_pages = request.GET.get("no_of_pages",None)
            page_no = request.GET.get("page_no",1)
            region = request.GET.get("region",None)
            per_page = request.GET.get("per_page",20)
            try:
                if not no_of_pages is None:
                    no_of_pages = int(no_of_pages)
                if  not page_no is None:
                    page_no = int(page_no)
                if not region is None:
                    region = str(region)
                if isinstance(per_page,str):
                    per_page = int(per_page)
            except Exception as e :
                print(e)
#
            listOfResultMovie = []

            
            movies =  Movies.objects.order_by("-release_date").all()
            pages = Paginator(movies,per_page)
        
            if no_of_pages is not None:
                for offset in range(no_of_pages):
                    
                    new_page_number = page_no + offset
                    if new_page_number <= pages.num_pages:
                        page = pages.get_page(new_page_number)
                        
                        for movie in page.object_list:
                            print(movie)
                            
                            listOfResultMovie.append(model_to_dict(movie))
                    else:
                        break
                data = {
                    "length": len(listOfResultMovie), 
                    "start_page_no":page_no,
                    "end_page_no":new_page_number-1,
                    "total_pages_fetched":new_page_number-page_no,

                    "total_pages":pages.num_pages,
                    "total_results":pages.count,
                    "results": listOfResultMovie
                }

            else:

                page = pages.get_page(page_no)

                for movie in page.object_list:
                    print(movie)
                    
                    listOfResultMovie.append(model_to_dict(movie))

                data = {
                    "length": len(listOfResultMovie), 
                    "start_page_no":page_no,
                    "end_page_no":page_no,
                    "total_pages_fetched":page_no-page_no+1,

                    "total_pages":pages.num_pages,
                    "total_results":pages.count,
                    "results": listOfResultMovie
                }

            

            return Response(data  )        

        except Exception as e :
            return Response({ "message":"Exception Occured error",
                "exception_class": str(e.__class__),},status=status.HTTP_400_BAD_REQUEST)

class get_movie_poster(APIView):
    def get(self, request,movie_id,format=None):
        try:
            poster_index = request.GET.get("poster_index",None)
            width = request.GET.get("width",None)
            language = request.GET.get("language",None)

            if poster_index is None:
                poster_index = 0
            else:
                poster_index = int(poster_index)
            if width is None:
                api = Tmdb_api()
                data,number_of_poster = api.get_movie_poster_images(movie_id,language=language,poster_index=poster_index)
                if data == None :
                    return Response({"message":f"{number_of_poster - 1} can be the highest value of poster_index"})
                else:
                    image = Image.open(io.BytesIO(data))
                    imgWidth , imgHeight = image.size
                   
                    height = int((16 / 9) * imgWidth)
                    image = image.resize((imgWidth,height))

                    byteIO = io.BytesIO()
                    image.save(byteIO,format="JPEG")

                    imageData = byteIO.getvalue()
                    return HttpResponse(io.BytesIO(imageData),content_type="image/jpeg")

            else:
                width = int(width)
                api = Tmdb_api()
                data,number_of_poster = api.get_movie_poster_images(movie_id,language=language,poster_index=poster_index)
                if data == None :
                    return Response({"message":f"{number_of_poster - 1} can be the highest value of poster_index"})
                else:
                    image = Image.open(io.BytesIO(data))
                    imgWidth , imgHeight = image.size

                    # height = int((imgHeight / imgWidth) * width)
                    # image = image.resize((width,height))
                    height = int((16 / 9) * width)
                    image = image.resize((width,height))

                    byteIO = io.BytesIO()
                    image.save(byteIO,format="JPEG")

                    imageData = byteIO.getvalue()
                    
                    return HttpResponse(io.BytesIO(imageData),content_type='image/jpeg')
        except Exception as e: 
           return Response({ "message":"Exception Occured error",
                "exception_class": str(e.__class__),},status=status.HTTP_400_BAD_REQUEST)

class get_movie_backdrop(APIView):
    def get(self,request,movie_id,format=None):
        try:
            width = request.GET.get("width",None)
            backdrop_index = int(request.GET.get("backdrop_index",0))
            
            if width is None:
                api = Tmdb_api()
                data,number_of_backdrops = api.get_movie_backdrop_images(movie_id,backdrop_index)
                if data == None :
                    return Response({"message":f"{number_of_backdrops - 1} can be the highest value of backdrop_index"})
                else:
                    image = Image.open(io.BytesIO(data))
                    imgWidth , imgHeight = image.size
                   
                    height = int((9 / 16) * imgWidth)
                    image = image.resize((imgWidth,height))

                    byteIO = io.BytesIO()
                    image.save(byteIO,format="JPEG")

                    imageData = byteIO.getvalue()

                    return HttpResponse(io.BytesIO(imageData),content_type='image/jpeg')

            else:
                width = int(width)
                api = Tmdb_api()
                data,number_of_backdrops = api.get_movie_backdrop_images(movie_id,backdrop_index)
                if data == None :
                    return Response({"message":f"{number_of_backdrops - 1} can be the highest value of backdrop_index"})
                else:
                    image = Image.open(io.BytesIO(data))
                    imgWidth , imgHeight = image.size

                    height = int((9 / 16) * width)
                    image = image.resize((width,height))

                    # height = int((imgHeight / imgWidth) * width)
                    # image = image.resize((width,height))
                
                    byteIO = io.BytesIO()
                    image.save(byteIO,format="JPEG")

                    imageData = byteIO.getvalue()
                    
                    return HttpResponse(io.BytesIO(imageData),content_type='image/jpeg')

        except Exception as e: 
           return Response({ "message":"Exception Occured error",
                "exception_class": str(e.__class__),},status=status.HTTP_400_BAD_REQUEST)


class get_movie_poster_urls(APIView):
    def get(self,request,movie_id,format=None):
        try:
            width = request.GET.get("width",None)
            language = request.GET.get("language",None)
            
            if width is None and language is None:
                api = Tmdb_api()
                data,number_of_poster = api.get_movie_poster_images(movie_id,language=language,only_index_length=True)
                listOfUrls = []
                for i in range(0,number_of_poster):
                    path  = reverse('ApiApp:movie_poster',args=[movie_id])
                    
                    url =f"http://{SERVER_NAME}{path}?poster_index={i}"
                    listOfUrls.append(url)

                return Response(listOfUrls,status=status.HTTP_200_OK)
            
            if width is not None and language is None:
                api = Tmdb_api()
                data,number_of_poster = api.get_movie_poster_images(movie_id,language=language,only_index_length=True)
                listOfUrls = []
                for i in range(0,number_of_poster):
                    path  = reverse('ApiApp:movie_poster',args=[movie_id])

                    url =f"http://{SERVER_NAME}{path}?poster_index={i}&width={width}"
                    listOfUrls.append(url)

                return Response(listOfUrls,status=status.HTTP_200_OK)
            
            if width is None and language is not None:
                api = Tmdb_api()
                data,number_of_poster = api.get_movie_poster_images(movie_id,language=language,only_index_length=True)
                listOfUrls = []
                for i in range(0,number_of_poster):
                    path  = reverse('ApiApp:movie_poster',args=[movie_id])

                    url =f"http://{SERVER_NAME}{path}?poster_index={i}&language={language}"
                    listOfUrls.append(url)

                return Response(listOfUrls,status=status.HTTP_200_OK)
            
            if width is not None and language is not None:
                api = Tmdb_api()
                data,number_of_poster = api.get_movie_poster_images(movie_id,language=language,only_index_length=True)
                listOfUrls = []
                for i in range(0,number_of_poster):
                    path  = reverse('ApiApp:movie_poster',args=[movie_id])

                    url =f"http://{SERVER_NAME}{path}?poster_index={i}&language={language}&width={width}"
                    listOfUrls.append(url)

                return Response(listOfUrls,status=status.HTTP_200_OK)
        
        except Exception as e: 
           return Response({ "message":"Exception Occured error",
                "exception_class": str(e.__class__),},status=status.HTTP_400_BAD_REQUEST)


class get_movie_backdrop_urls(APIView):
    def get(self,request,movie_id,format=None):
        try:
            width = request.GET.get("width",None)
            if width is None:
                api = Tmdb_api()
                data,number_of_backdrops = api.get_movie_backdrop_images(movie_id,only_index_length=True)
                listOfUrls = []
                for i in range(0,number_of_backdrops):
                    path  = reverse('ApiApp:movie_backdrop',args=[movie_id])

                    url =f"http://{SERVER_NAME}{path}?backdrop_index={i}"
                    listOfUrls.append(url)

                return Response(listOfUrls,status=status.HTTP_200_OK)

            else:
                width = int(width)
                api = Tmdb_api()
                data,number_of_backdrops = api.get_movie_backdrop_images(movie_id,only_index_length=True)
                listOfUrls = []
                for i in range(0,number_of_backdrops):
                    path  = reverse('ApiApp:movie_backdrop',args=[movie_id])

                    url =f"http://{SERVER_NAME}{path}?backdrop_index={i}&width={width}"
                    listOfUrls.append(url)
                return Response(listOfUrls,status=status.HTTP_200_OK)

        except Exception as e: 
           return Response({ "message":"Exception Occured error",
                "exception_class": str(e.__class__),},status=status.HTTP_400_BAD_REQUEST)


class get_complete_movie_details(APIView):
    def get(self,request,movie_id,format=None):    
        try: 
            width = request.GET.get("width",None)

            myDB = Database()  
            movie = myDB.get_movies_from_id(ID = movie_id)
            api = Tmdb_api()
           
            
            urls = get_movie_backdrop_urls().get(request,movie_id)
            if urls.data:
                movie["backdrop_urls"] =  urls.data
            urls = get_movie_poster_urls().get(request,movie_id)

            if urls.data:

                movie["poster_urls"] =  urls.data

            movie["genres"] = myDB.get_movie_genres(ID=movie_id)

            mySOures = MovieSources()
            movie["sources"] = mySOures.get_sources(movie_id)
           


            return Response(movie)
            

        except Exception as e: 
           return Response({ "message":"Exception Occured error",
                "exception_class": str(e.__class__),},status=status.HTTP_400_BAD_REQUEST)


class search_movie(APIView):
    def get(self,request,format=None):
        try:
            query = request.GET.get("query",None)
            language =  request.GET.get("language",None)
            page =  request.GET.get("page",1)
            include_adult  =  request.GET.get("include_adult",None)
            region  =  request.GET.get("region",None)
            year =  request.GET.get("year",None)
            primary_release_year =  request.GET.get("primary_release_year",None)
            fetch_length = request.GET.get("fetch_length",0)
            
            if isinstance(page,str):
                page = int(page)

            if include_adult is not None:
                include_adult = bool(include_adult)
            
            if isinstance(year,str):
                year = int(year)
           
            if isinstance(primary_release_year,str):
                primary_release_year = int(primary_release_year)
            
            if isinstance(fetch_length,str):
                fetch_length = int(fetch_length)

            loop_counter = 0
            found_null = 0
            search_result = []

            if query is not None:
                while True:
                    loop_counter == 1
                    api =Tmdb_api()
                    
                
                    for movie in api.search_movie(query,language,page,include_adult,region,year,primary_release_year):
                        if SYSTEM_MOVIE_ID is not None:
                            if movie.get("id") in SYSTEM_MOVIE_ID:
                                response = get_complete_movie_details().get(request,movie_id=movie.get("id"))
                                if response.data is not None:
                                    search_result.append(response.data)
                                    found_null = 0
                        
                        else:
                            if movie.get("id") in list(Database().get_all_movie_ids()):
                                response = get_complete_movie_details(request,movie_id=movie.get("id"))
                                if response.data is not None:
                                    search_result.append(response.data)
                                    found_null = 0
                        
                
                    if len(search_result) >= fetch_length or found_null >= 10:
                            break
                    else:
                        page = page + 1
                        found_null += 1



                return Response({"total_results":len(search_result),
                                "results":search_result})

        except Exception as e: 
           return Response({ "message":"Exception Occured error",
                "exception_class": str(e.__class__),},status=status.HTTP_400_BAD_REQUEST)

class  movie_credits(APIView):
    def get(self,request,movie_id,format=None):
        # try:
            api = Tmdb_api()
            cast,crew= api.get_movie_credits(movie_id)
            return Response({"id":movie_id,"cast":cast,
            "crew":crew})
        # except :
            # pass

class similar_movies(APIView):
    def get(self,request,movie_id,format=None):
        language =  request.GET.get("language",None)
        page =  request.GET.get("page",1)
        fetch_length = request.GET.get("fetch_length",1)  

        if isinstance(page,str):
            page = int(page)
        if isinstance(fetch_length,str):
            fetch_length = int(fetch_length)

        api = Tmdb_api()
        myDb = Database()   
        listOfMovies = []
        while len(listOfMovies) < fetch_length:
            JSON = api.get_similar_movies(movie_id,language,page)
            total_pages = JSON.get("total_pages")
            for movieJson in JSON.get("results") :
                ID = movieJson.get("id")
                if ID in SYSTEM_MOVIE_ID: 
                    result = myDb.get_movies_from_id(ID = ID)
                    listOfMovies.append(result)
            page += 1
            if page > total_pages:
                break



        return Response({"length":len(listOfMovies),"results":listOfMovies})
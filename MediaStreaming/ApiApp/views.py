from django.shortcuts import render
from rest_framework import viewsets

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *

from rest_framework import status
from django.http import Http404

from .database import Database

from django.forms.models import model_to_dict
from .app_settings  import SERVER_NAME,SYSTEM_MOVIE_ID,SYSTEM_PEOPLE_ID
from django.conf import settings
from django.urls import URLPattern, URLResolver
from django.contrib.sites.shortcuts import get_current_site
urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])

from django.urls import path,include


SYSTEM_MOVIE_ID = Database().get_all_movie_ids()
SYSTEM_PEOPLE_ID = Database().get_all_people_ids()





class ApiHome(APIView):
    def list_urls(self,lis, acc=None):
        if acc is None:
            acc = []
        if not lis:
            return
        l = lis[0]
        if isinstance(l, URLPattern):
            yield acc + [str(l.pattern)]
        elif isinstance(l, URLResolver):
            yield from self.list_urls(l.url_patterns, acc + [str(l.pattern)])
        yield from self.list_urls(lis[1:], acc)
    def get(self,request,format=None):


        urls = []
        for Url in include('ApiApp.urls')[0].urlpatterns:
            url = f"{request.scheme}://{SERVER_NAME}/api/{Url.pattern._route}"
            urls.append(url)
        return Response(urls)

class MovieApi(viewsets.ModelViewSet):
    serializer_class = MoviesSerializer
    queryset = Movies.objects.all()[:10]

class UserApi(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    queryset = Users.objects.all()[:10]

class UserApiTest(APIView):
    def get(self,request,format=None):
        users = Users.objects.all()
        serializer = UsersSerializer(users ,many=True)
        
        movie =   Movies.objects.get(id=5)
        genres = movie.moviestogenres_set
        result = model_to_dict(movie)
        print(result)
        return Response(serializer.data)

    def post(self,request,format=None):
        serializer = UsersSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

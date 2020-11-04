from rest_framework.views import APIView
from rest_framework.response import Response

from .external_apis import Tmdb_api
from .database import Database
from .sources import MovieSources
from .views import SYSTEM_PEOPLE_ID,SYSTEM_MOVIE_ID
from django.http import HttpResponse
import io
from PIL import  Image
import rest_framework
from rest_framework import status
from django.urls import reverse,reverse_lazy


from django.contrib.sites.shortcuts import get_current_site


from .app_settings  import SERVER_NAME
import firebase_admin
from firebase_admin import auth,credentials

import requests


class Users(APIView):
    permission_classes  = [rest_framework.permissions.AllowAny]
    def post(self,request,format=None):
        try:
            
            token = request.GET.get("token",None)
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            user = auth.get_user(uid)

            profilePicture = None
            if user.photo_url:
                r = requests.get(user.photo_url)
                if r.status_code == 200:
                    profilePicture = r.content

            myDB = Database()
            user_save_result = myDB.create_new_user(uid,name=user.display_name,email=user.email,full_phone_number=user.phone_number,profile_picture=profilePicture)
        
            return Response(user_save_result)
        except firebase_admin._auth_utils.InvalidIdTokenError as e:

            result = {
                "status":False,
                "msg":e.default_message,
                "Expection Class Name":str(e.__class__.__name__),
                "Expection Class ":str(e.__class__)

            }
            return Response(result)

  

class Users_History(APIView):
    permission_classes  = [rest_framework.permissions.AllowAny]

    def get(self,request,format=None):
        try:
            token = request.GET.get("token",None)
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            user = auth.get_user(uid)


            return Response(uid)
        except firebase_admin._auth_utils.InvalidIdTokenError as e:

            result = {
                "status":False,
                "msg":e.default_message,
                "Expection Class Name":str(e.__class__.__name__),
                "Expection Class ":str(e.__class__)

            }
            return Response(result)
        except Exception as e:
            
            result = {
                "status":False,
                "msg":e.args,
                "Expection Class Name":str(e.__class__.__name__),
                "Expection Class ":str(e.__class__)

            }
            return Response(result)

    def post(self,request,format=None):
        try:
            
            token = request.GET.get("token",None)
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            user = auth.get_user(uid)
            data_dict = request.data
            

            
           
            return Response(request.data)
        except firebase_admin._auth_utils.InvalidIdTokenError as e:

            result = {
                "status":False,
                "msg":e.default_message,
                "Expection Class Name":str(e.__class__.__name__),
                "Expection Class ":str(e.__class__)

            }
            return Response(result)
        except  Exception as e:
            result = {
                "status":False,
                "msg":e.args,
                "Expection Class Name":str(e.__class__.__name__),
                "Expection Class ":str(e.__class__)

            }
            return Response(result)

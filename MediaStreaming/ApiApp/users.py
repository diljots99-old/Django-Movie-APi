from rest_framework.views import APIView
from rest_framework.response import Response

from .external_apis import Tmdb_api
from .database import Database
from .sources import MovieSources
from .views import SYSTEM_PEOPLE_ID,SYSTEM_MOVIE_ID
from .models import *
from .models import Users as dbUsers
from django.http import HttpResponse
import io
from PIL import  Image
import rest_framework
from rest_framework import status
from django.urls import reverse,reverse_lazy


from django.contrib.sites.shortcuts import get_current_site

import datetime
from .app_settings  import SERVER_NAME
import firebase_admin
from firebase_admin import auth,credentials
from django.forms.models import model_to_dict

import requests



class updateVerifiedUser(APIView):
    permission_classes  = [rest_framework.permissions.AllowAny]
    def get(self,request,format=None):
        try:
            
            token = request.GET.get("token",None)
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            user = auth.get_user(uid)
            
            dbUser = dbUsers.objects.filter(uid=uid)

            for  dbuser in dbUser:

                auth.update_user(
                    uid,
                    email=user.email,
                    email_verified=True
                )
                return HttpResponse(f"{user.email} Verifed Succesfully")


        except firebase_admin._auth_utils.InvalidIdTokenError as e:

            result = {
                "status":False,
                "msg":e.default_message,
                "Expection Class Name":str(e.__class__.__name__),
                "Expection Class ":str(e.__class__)

            }
            return Response(result)
    


class Users(APIView):
    permission_classes  = [rest_framework.permissions.AllowAny]

    def get(self,request,format=None):
        try:
            
            token = request.GET.get("token",None)
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            user = auth.get_user(uid)

            dbUser = dbUsers.objects.filter(uid=uid)
            
            profilePicture = None
            if user.photo_url:
                r = requests.get(user.photo_url)
                if r.status_code == 200:
                    profilePicture = r.content

            for  dbuser in dbUser:
                dbuser.name=user.display_name
                dbuser.email=user.email
                dbuser.full_phone_number=user.phone_number
                dbuser.profile_picture=profilePicture
                dbuser.save()
                return Response(model_to_dict(dbuser))

        except firebase_admin._auth_utils.InvalidIdTokenError as e:

            result = {
                "status":False,
                "msg":e.default_message,
                "Expection Class Name":str(e.__class__.__name__),
                "Expection Class ":str(e.__class__)

            }
            return Response(result)

    def put(self,request,format=None):
        try:
            
            token = request.GET.get("token",None)
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            user = auth.get_user(uid)
            
            dbUser = dbUsers.objects.filter(uid=uid)
            
       
            profilePicture = None
            if user.photo_url:
                r = requests.get(user.photo_url)
                if r.status_code == 200:
                    profilePicture = r.content
            
            for  dbuser in dbUser:
                dbuser.name=user.display_name
                dbuser.email=user.email
                dbuser.full_phone_number=user.phone_number
                dbuser.profile_picture=profilePicture
                dbuser.save()
                return Response(model_to_dict(dbuser))

        except firebase_admin._auth_utils.InvalidIdTokenError as e:

            result = {
                "status":False,
                "msg":e.default_message,
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

    def get(self,request,pk,format=None):
        try:
            uid = pk
            token = request.GET.get("token",None)
            decoded_token = auth.verify_id_token(token)
            decoded_uid = decoded_token['uid']
            if decoded_uid == uid:
                user = auth.get_user(uid)
                user_history_query_set = UserHistory.objects.filter(uid=uid).order_by("-last_accessed").all()

                user_history = []
                for history in user_history_query_set.iterator():
                    
                    historyJSON = model_to_dict(history)

                    if historyJSON.get("type") == "movie":
                        historyJSON["data"] = {}

                        try:
                            movie = Movies.objects.get(id=historyJSON.get("backref_id"))

                            if not movie is None:
                                historyJSON["data"] = model_to_dict(movie)

                        except :
                            pass
                    user_history.append(historyJSON)

                return Response(user_history)

            return Response([])
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

    def post(self,request,pk,format=None):
        try:
            uid = pk
            token = request.GET.get("token",None)
            decoded_token = auth.verify_id_token(token)
            decoded_uid = decoded_token['uid']
            user = auth.get_user(decoded_uid)
            data_dict = request.data
            if uid == decoded_uid:
                tYpe = data_dict.get("type")
                backref_id = data_dict.get("backref_id")
                date_created = data_dict.get("date_created")
                last_accessed = date_created

                if date_created is None:
                    date_created  = datetime.datetime.now()
                    last_accessed = date_created
 
                if  (uid is not None) and (tYpe is not None) and (backref_id is not None):
                    user = dbUsers.objects.get(uid=uid)
                    user_history =  UserHistory(uid=user,type=tYpe,backref_id=backref_id,date_created=date_created,last_accessed=last_accessed)
                    user_history.save()
                    result = {
                    "status":True,
                    "msg":"Data Saved"
                                    
                    }
                    return Response(result)

                result = {
                "status":False,
                "msg":"UID  match"
                
                }
                return Response(result)
                
            else :
                result = {
                "status":False,
                "msg":"UID Does not match"
                
                }
                return Response(result)
           
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
    def put(self,request,pk,format=None):
        try:
            ID = int(pk)
            token = request.GET.get("token",None)
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            user = auth.get_user(uid)
            data_dict = request.data
            if uid == data_dict.get("uid"):

                last_accessed = datetime.datetime.now()
                user_history = UserHistory.objects.get(id=ID)
                user_history.last_accessed  = last_accessed
                user_history.save()
                

               

                result = {
                "status":True,
                "msg":"last_accessed updated"
                
                }
                return Response(result)
                
            else :
                result = {
                "status":False,
                "msg":"UID Does not match"
                
                }
                return Response(result)
           
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
    def delete(self,request,pk,format=None):
        try:
            ID = int(pk)
            token = request.GET.get("token",None)
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            user = auth.get_user(uid)
            data_dict = request.data
            if uid == data_dict.get("uid"):

                last_accessed = datetime.datetime.now()
                user_history = UserHistory.objects.get(id=ID)
                user_history.last_accessed  = last_accessed
                user_history.delete()
                

                result = {
                "status":True,
                "msg":f"User History with id {ID} Deleted"
                
                
                }
                return Response(result)
                
            else :
                result = {
                "status":False,
                "msg":"UID Does not match"
                
                }
                return Response(result)
           
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



class Users_Favourites(APIView):
    permission_classes  = [rest_framework.permissions.AllowAny]

    def get(self,request,pk,format=None):
        try:
            uid = pk
            token = request.GET.get("token",None)
            decoded_token = auth.verify_id_token(token)
            decoded_uid = decoded_token['uid']
            if decoded_uid == uid:
                user = auth.get_user(uid)
                user_favourites_query_set = UserFavourites.objects.filter(uid=uid).order_by("-last_accessed").all()

                user_favourites = []
                for history in user_favourites_query_set.iterator():
                    user_favourites.append(model_to_dict(history))

                return Response(user_favourites)

            return Response([])
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

    def post(self,request,pk,format=None):
        try:
            uid = pk
            token = request.GET.get("token",None)
            decoded_token = auth.verify_id_token(token)
            decoded_uid = decoded_token['uid']
            user = auth.get_user(decoded_uid)
            data_dict = request.data
            if uid == decoded_uid:
                tYpe = data_dict.get("type")
                backref_id = data_dict.get("backref_id")
                date_created = data_dict.get("date_created")
                last_accessed = date_created

                if date_created is None:
                    date_created  = datetime.datetime.now()
                    last_accessed = date_created
 
                if  (uid is not None) and (tYpe is not None) and (backref_id is not None):
                    user = dbUsers.objects.get(uid=uid)
                    user_favourites =  UserFavourites(uid=user,type=tYpe,backref_id=backref_id,date_created=date_created,last_accessed=last_accessed)
                    user_favourites.save()
                    result = {
                    "status":True,
                    "msg":"Data Saved"
                                    
                    }
                    return Response(result)

                result = {
                "status":False,
                "msg":"UID  match"
                
                }
                return Response(result)
                
            else :
                result = {
                "status":False,
                "msg":"UID Does not match"
                
                }
                return Response(result)
           
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
    def put(self,request,pk,format=None):
        try:
            ID = int(pk)
            token = request.GET.get("token",None)
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            user = auth.get_user(uid)
            data_dict = request.data
            if uid == data_dict.get("uid"):

                last_accessed = datetime.datetime.now()
                user_favourites = UserFavourites.objects.get(id=ID)
                user_favourites.last_accessed  = last_accessed
                user_favourites.save()
                

               

                result = {
                "status":True,
                "msg":"last_accessed updated"
                
                }
                return Response(result)
                
            else :
                result = {
                "status":False,
                "msg":"UID Does not match"
                
                }
                return Response(result)
           
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
    def delete(self,request,pk,format=None):
        try:
            ID = int(pk)
            token = request.GET.get("token",None)
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            user = auth.get_user(uid)
            data_dict = request.data
            if uid == data_dict.get("uid"):

                last_accessed = datetime.datetime.now()
                user_favourites = UserFavourites.objects.get(id=ID)
                user_favourites.delete()
                

               

                result = {
                "status":True,
                "msg":f"User Favourites with id {ID} Deleted"
                
                }
                return Response(result)
                
            else :
                result = {
                "status":False,
                "msg":"UID Does not match"
                
                }
                return Response(result)
           
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

class Users_Watchlist(APIView):
    permission_classes  = [rest_framework.permissions.AllowAny]

    def get(self,request,pk,format=None):
        try:
            uid = pk
            token = request.GET.get("token",None)
            decoded_token = auth.verify_id_token(token)
            decoded_uid = decoded_token['uid']
            if decoded_uid == uid:
                user = auth.get_user(uid)
                user_watchlist_query_set = UserWatchlist.objects.filter(uid=uid).order_by("-last_accessed").all()

                user_watchlist = []
                for history in user_watchlist_query_set.iterator():
                    user_watchlist.append(model_to_dict(history))

                return Response(user_watchlist)

            return Response([])
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

    def post(self,request,pk,format=None):
        try:
            uid = pk
            token = request.GET.get("token",None)
            decoded_token = auth.verify_id_token(token)
            decoded_uid = decoded_token['uid']
            user = auth.get_user(decoded_uid)
            data_dict = request.data
            if uid == decoded_uid:
                tYpe = data_dict.get("type")
                backref_id = data_dict.get("backref_id")
                date_created = data_dict.get("date_created")
                last_accessed = date_created

                if date_created is None:
                    date_created  = datetime.datetime.now()
                    last_accessed = date_created
 
                if  (uid is not None) and (tYpe is not None) and (backref_id is not None):
                    user = dbUsers.objects.get(uid=uid)
                    user_watchlist =  UserWatchlist(uid=user,type=tYpe,backref_id=backref_id,date_created=date_created,last_accessed=last_accessed)
                    user_watchlist.save()
                    result = {
                    "status":True,
                    "msg":"Data Saved"
                                    
                    }
                    return Response(result)

                result = {
                "status":False,
                "msg":"UID  match"
                
                }
                return Response(result)
                
            else :
                result = {
                "status":False,
                "msg":"UID Does not match"
                
                }
                return Response(result)
           
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
    def put(self,request,pk,format=None):
        try:
            ID = int(pk)
            token = request.GET.get("token",None)
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            user = auth.get_user(uid)
            data_dict = request.data
            if uid == data_dict.get("uid"):

                last_accessed = datetime.datetime.now()
                user_watchlist = UserWatchlist.objects.get(id=ID)
                user_watchlist.last_accessed  = last_accessed
                user_watchlist.save()
                

               

                result = {
                "status":True,
                "msg":"last_accessed updated"
                
                }
                return Response(result)
                
            else :
                result = {
                "status":False,
                "msg":"UID Does not match"
                
                }
                return Response(result)
           
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
    def delete(self,request,pk,format=None):
        try:
            ID = int(pk)
            token = request.GET.get("token",None)
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            user = auth.get_user(uid)
            data_dict = request.data
            if uid == data_dict.get("uid"):

                last_accessed = datetime.datetime.now()
                user_watchlist = UserWatchlist.objects.get(id=ID)
                user_watchlist.delete()
                

               

                result = {
                "status":True,
                "msg":f"User Watchlist with id {ID} Deleted"
                
                }
                return Response(result)
                
            else :
                result = {
                "status":False,
                "msg":"UID Does not match"
                
                }
                return Response(result)
           
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
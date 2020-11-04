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

class get_people_profile_picture(APIView):
    def get(self,request,people_id,format=None):
        try:
            width = request.GET.get("width",None)

            if isinstance(width,str):
                width = int(width)
            api = Tmdb_api()
            myDB = Database()

            people = myDB.get_people_details(people_id)
            if width is None:
                image = Image.open(io.BytesIO(people["profile_picture"]))
                imgWidth , imgHeight = image.size

                # height = int( (imgHeight / imgWidth) * width)
                # image = image.resize((width,height))
                height = int((16 / 9) * imgWidth)
                image = image.resize((imgWidth,height))
            
                byteIO = io.BytesIO()
                image.save(byteIO,format="JPEG")

                imageData = byteIO.getvalue()
                return HttpResponse(io.BytesIO(people["profile_picture"]),content_type="image/jpeg")
                
            else:
                image = Image.open(io.BytesIO(people["profile_picture"]))
                imgWidth , imgHeight = image.size

                # height = int( (imgHeight / imgWidth) * width)
                # image = image.resize((width,height))
                height = int((16 / 9) * imgWidth)
                image = image.resize((imgWidth,height))

                byteIO = io.BytesIO()
                image.save(byteIO,format="JPEG")

                imageData = byteIO.getvalue()

                return HttpResponse(io.BytesIO(imageData),content_type="image/jpeg")
                
                
        

        except Exception as e: 
          return Response({ "message":"Exception Occured error",
                "exception_class": str(e.__class__),} )

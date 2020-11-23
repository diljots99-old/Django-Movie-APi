from rest_framework.views import APIView
from rest_framework.response import Response

from .external_apis import Tmdb_api
from .database import Database
from .sources import MovieSources
from .views import SYSTEM_PEOPLE_ID,SYSTEM_MOVIE_ID
from django.http import HttpResponse,FileResponse
import io
from PIL import  Image
import rest_framework
from rest_framework import status
from django.urls import reverse,reverse_lazy


from django.contrib.sites.shortcuts import get_current_site


from .app_settings  import SERVER_NAME

class get_torrent_file(APIView):
    def get(self,request,torrent_id,format=None):
            try:
                MyDB =Database()
                torrent = MyDB.get_torrent_by_id(torrent_id)
                # response = FileResponse(torrent.get("torrent_file"),as_attachment=True, filename=f'{torrent_id}.torrent',content_type="application/x-bittorrent")
                torrent_file = torrent.get("torrent_file")
                # response = FileResponse(io.BytesIO(torrent_file),content_type="application/x-bittorrent")
                response = FileResponse((torrent_file),content_type="application/x-bittorrent")
                response =  HttpResponse(io.BytesIO(torrent_file),content_type='application/x-bittorrent')
                
                response['Content-Disposition'] = f'attachment; filename="{torrent_id}.torrent"'
                return     response           


            except Exception as e: 
                return Response({ "message":"Exception Occured error",
                        "exception_class": str(e.__class__),} )

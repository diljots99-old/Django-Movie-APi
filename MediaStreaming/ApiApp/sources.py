from .database import Database
from .firebase import FirebaseSources

from django.forms.models import model_to_dict

class MovieSources():
    def __init__(self):
        pass


    def get_torrets(self,movie_id):

        listOfTosrrent =  Database().get_torrents_from_movie_id(movie_id)
        return listOfTosrrent

    def get_google_drive(self,movie_id):

        listOfTosrrent =  Database().get_google_drive_from_movie_id(movie_id)
        return listOfTosrrent
    def get_firebase(self,movie_id):
        try:
            listOfTosrrent =  Database().get_firebase_from_movie_id(movie_id)
            firebaseListWithAdminurls =[]
            for source in listOfTosrrent:
                credentialsJSON = model_to_dict(source.credentials)
                url = FirebaseSources(credentialsJSON).get_public_url(source.file_path)
                sourceJSON = model_to_dict(source)
                sourceJSON["public_url"] = url
                firebaseListWithAdminurls.append(sourceJSON)

            return firebaseListWithAdminurls
        except Exception as e:
            return []

    def get_sources(self,movie_id):
        try:
            torrents = self.get_torrets(movie_id)
            driveFiles = self.get_google_drive(movie_id)
            firebaseList = self.get_firebase(movie_id)
            


            sources = {}
            sources["torrents"] = torrents 

            sources["Drive"] = driveFiles    
            sources["firebase"] = firebaseList 
    
    
            return sources
        except:
            return None
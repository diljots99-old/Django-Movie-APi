from .database import Database

class MovieSources():
    def __init__(self):
        pass


    def get_torrets(self,moive_id):

        listOfTosrrent =  Database().get_torrents_from_movie_id(moive_id)

       
        return listOfTosrrent
            
    def get_sources(self,moive_id):
        try:
            torrents = self.get_torrets(moive_id)
            sources = {}
            if len(torrents) > 0:
                sources["torrents"] = torrents 

            return sources
        except:
            return None
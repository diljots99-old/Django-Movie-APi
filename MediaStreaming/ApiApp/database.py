from .models import Movies,MoviesToGenres,Genres,MoviesToTorrents
from .models import *
from .serializers import PeopleSerializer
from ApiApp import views
from django.forms.models import model_to_dict



class Database():
    def __init__(self):
        pass
    
    def get_movies_from_id(self,ID=None):
            if ID is not None:
                try:
                    movie = Movies.objects.get(id=ID)
                    result = model_to_dict(movie)
                    return result
                except Exception as e:
                    return None
               

            else:
                return None

    def get_movie_genres(self,ID):
        try:
            
            mass = MoviesToGenres.objects.filter(movie_id=ID).all()
            list_of_genres = []
            list_of_genres_id = []

            for value in mass:
                # genre = Genres.objects.get(id=value.genre
                genre = value.genre
                
                if  len(list_of_genres_id) <1:
                    list_of_genres_id.append(genre.id)
                    list_of_genres.append(model_to_dict(genre))

                else:
                    if not genre.id in list_of_genres_id:
                        list_of_genres.append(model_to_dict(genre))
                        list_of_genres_id.append(genre.id)


                

            return list_of_genres
        except Exception as e:
            return []

    def get_torrents_from_movie_id(self,ID= None):
        if ID is not None:
            mot = MoviesToTorrents.objects.all().filter(movie_id=ID).values()
            list_of_torrents = []
            
            for value in mot.iterator():
                torrent = Torrents.objects.get(id=value['torrent_id'])
            
                list_of_torrents.append(model_to_dict(torrent))
            return list_of_torrents
        else:
            return []
    


    def get_all_movie_ids(self):
        movies = Movies.objects.only("id")     
        
        RESULT = []
        for movie in movies.iterator():
            RESULT.append(movie.id)


        return RESULT

    def get_all_people_ids(self):
        peoples = People.objects.only("id")
        
        RESULT = []
        for people in peoples.iterator():
            RESULT.append(people.id)
        return RESULT

    def add_people(self,people_json,profile_picture=None):
        try:
            data = {
                "id": people_json["id"],
                "birthday": people_json["birthday"],
                "known_for_department" : people_json['known_for_department'],
                "death_day": people_json['deathday'],
                "name" : people_json['name'],
                "gender" :people_json['gender'],
                "popularity" : people_json['popularity'],
                "imdb_id" :people_json['imdb_id'],
                "homepage" : people_json['homepage'],
                "place_of_birth" : people_json['place_of_birth'],
                "profile_picture" : people_json["profile_picture"],
                "biography" : people_json['biography'],
                "adult" : people_json['adult'],
                "profile_picture_path" : people_json['profile_path']
            }
            people = People(**data)
            
            people.save()
            print(people.id)
            
            

            # people.save()
            views.SYSTEM_PEOPLE_ID.append(int(people.id))
            
        except Exception as e:
            print ("expetion occured")

    def create_new_user(self,UID,name=None,email=None,full_phone_number=None,profile_picture=None):
        try:
            
            user  = Users (UID,name,email,full_phone_number,profile_picture)       
            user.save(force_insert=True)
                      
            return {"status": True,"msg":"User Data Saved","Expection Class Name":None,
                "Expection Class ":None}

        
        except Exception as e:
            
            return {"status": False,"msg":"Some Other Error","Expection Class Name":str(e.__class__.__name__),
                "Expection Class ":str(e.__class__)}
    
    def get_people_details(self,people_id):
        if people_id is not None:
                try:
                    people = People.objects.get(id=people_id)
                    result = model_to_dict(people)
                    result["profile_picture"] = people.profile_picture
                    return result
                except:
                    return None
        else:
                return None
    def get_torrent_by_id(self,torrent_id):
        if torrent_id is not None:
                try:
                    torrent = Torrents.objects.get(id=torrent_id)
                    result = model_to_dict(torrent)
                    result["torrent_file"] = torrent.torrent_file
                    return result
                except:
                    return None
        else:
                return None

    def get_google_drive_from_movie_id(self,ID):
        try:
            mot = SourceGoogleDrive.objects.filter(backref_id=ID).values()
            list_of_Drive_Files =  []

            for value in mot.iterator():
                
                list_of_Drive_Files.append(value)
            return list_of_Drive_Files
            
          
        except:
            return []

    def get_firebase_from_movie_id(self,ID):
        try:
            movie = Movies.objects.get(id=ID)
            mot = FirebaseMovies.objects.filter(movie=movie).all()
            list_of_Drive_Files =  []

            for value in mot.iterator():
                
                list_of_Drive_Files.append(value)
            return list_of_Drive_Files
            
          
        except:
            return []
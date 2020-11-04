import requests ,pprint
# from FlaskApp import app

# from FlaskApp.database import Database
import threading
from ApiApp import  views
from .database import Database
class Yts_Api:
    def __init__(self):
        pass
    
   
    def get_movies_form_list(self,page_no=None):
        
        if page_no==None:
            url = f'https://yts.mx/api/v2/list_movies.json'
        else:
            url = f'https://yts.mx/api/v2/list_movies.json?page={page_no}'
        
            
        r = requests.get(url)
        if r.status_code == 200:
            try:
                ytsJSON = r.json()
                return ytsJSON["data"]["movies"]
            except:
                return []
        else:
            return []


class Tmdb_api:
    def __init__(self):
        self.TMDB_API_KEY = "3f07b0ab597dec3ed6f9793b4087111a"


    def get_now_playing_movies(self,no_of_pages=None,page_no=None,region=None):

        baseURL = f"https://api.themoviedb.org/3/movie/now_playing?api_key={self.TMDB_API_KEY}"

        if no_of_pages is not None:
            no_of_pages = int(no_of_pages)

        if region is not None:
                baseURL == baseURL + f"&region={region}"
            
        if no_of_pages == None or no_of_pages == 1:
            if page_no is None:
                page_no = 1
            
            url = baseURL + f"&page={page_no}"
           
            r = requests.get(url)
            if r.status_code == 200:
                resultJSON = r.json()

                return list(resultJSON.get("results"))
            else:
                return []
        
        if no_of_pages > 1:
            
            if page_no is None:
                page_no = 1
            
            listOfMovies =[]
            for i in range(int(no_of_pages)):
                url = baseURL + f"&page={page_no}"
                r = requests.get(url)
                if r.status_code == 200:
                    resultJSON = r.json()
                    listOfMovies.extend(resultJSON.get("results"))
                page_no = page_no + 1

            return listOfMovies
    
    def get_popular_movies(self,no_of_pages=None,page_no=None,region=None):

        baseURL = f"https://api.themoviedb.org/3/movie/popular?api_key={self.TMDB_API_KEY}"

        if no_of_pages is not None:
            no_of_pages = int(no_of_pages)

        if region is not None:
                baseURL == baseURL + f"&region={region}"
            
        if no_of_pages == None or no_of_pages == 1:
            if page_no is None:
                page_no = 1
            
            url = baseURL + f"&page={page_no}"
           
            r = requests.get(url)
            if r.status_code == 200:
                resultJSON = r.json()

                return list(resultJSON.get("results"))
            else:
                return []
        
        if no_of_pages > 1:
            
            if page_no is None:
                page_no = 1
            
            listOfMovies =[]
            for i in range(int(no_of_pages)):
                url = baseURL + f"&page={page_no}"
                r = requests.get(url)
                if r.status_code == 200:
                    resultJSON = r.json()
                    listOfMovies.extend(resultJSON.get("results"))
                page_no = page_no + 1

            return listOfMovies
    def get_top_rated_movies(self,no_of_pages=None,page_no=None,region=None):

        baseURL = f"https://api.themoviedb.org/3/movie/top_rated?api_key={self.TMDB_API_KEY}"

        if no_of_pages is not None:
            no_of_pages = int(no_of_pages)

        if region is not None:
                baseURL == baseURL + f"&region={region}"
            
        if no_of_pages == None or no_of_pages == 1:
            if page_no is None:
                page_no = 1
            
            url = baseURL + f"&page={page_no}"
           
            r = requests.get(url)
            if r.status_code == 200:
                resultJSON = r.json()

                return list(resultJSON.get("results"))
            else:
                return []
        
        if no_of_pages > 1:
            
            if page_no is None:
                page_no = 1
            
            listOfMovies =[]
            for i in range(int(no_of_pages)):
                url = baseURL + f"&page={page_no}"
                r = requests.get(url)
                if r.status_code == 200:
                    resultJSON = r.json()
                    listOfMovies.extend(resultJSON.get("results"))
                page_no = page_no + 1

            return listOfMovies


    def get_movie_poster_images(self,movie_id,poster_index=0,language=None,only_index_length=False):
        baseUrl =f"https://api.themoviedb.org/3/movie/{movie_id}/images?api_key={self.TMDB_API_KEY}"

        sameLanguageImageFound = False
        r = requests.get(baseUrl)

        
        if r.status_code == 200:
            resultJSON =r.json()
            postersJSON = list(resultJSON.get("posters"))

            postersJSON = sorted(postersJSON ,key = lambda i: i["height"])
            postersJSON.reverse()
        
            if language is None:

                
                if poster_index < len(postersJSON):
                    filePath = postersJSON[poster_index].get("file_path")
                    baseImageURL ="https://image.tmdb.org/t/p/original"
                    url = baseImageURL + filePath
                if not only_index_length:

                        rjpeg = requests.get(url)
                        if rjpeg.status_code == 200:
                            return  rjpeg.content,len(postersJSON)
                        else:
                            return  None,len(postersJSON)
        
                else:
                    return  None,len(postersJSON)
                
            if language is not None:
                filteredPosterJSON = []         
                for jsonITEM in postersJSON:
                    if jsonITEM.get("iso_639_1") == language:
                        filteredPosterJSON.append(jsonITEM)
                filteredPosterJSON.reverse()
                if poster_index < len(filteredPosterJSON):        
                    filePath = filteredPosterJSON[poster_index].get("file_path")
                    baseImageURL ="https://image.tmdb.org/t/p/original"
                    url = baseImageURL + filePath
                    if not only_index_length:

                        rjpeg = requests.get(url)
                        if rjpeg.status_code == 200:
                            return  rjpeg.content,len(filteredPosterJSON)
                    else:
                        return  None,len(filteredPosterJSON)
                else:
                    return  None,len(filteredPosterJSON)
                

    def get_movie_backdrop_images(self,movie_id,backdrop_index=0,only_index_length=False ):
        baseUrl =f"https://api.themoviedb.org/3/movie/{movie_id}/images?api_key={self.TMDB_API_KEY}"

        sameLanguageImageFound = False
        r = requests.get(baseUrl)
        if r.status_code == 200:
            if not only_index_length:
                resultJSON =r.json()
                backdropsJSON = list(resultJSON.get("backdrops"))

                backdropsJSON = sorted(backdropsJSON ,key = lambda i: i["width"])
                backdropsJSON.reverse()

                if backdrop_index < len(backdropsJSON):
                    
                    filePath = backdropsJSON[backdrop_index].get("file_path")
                    baseImageURL ="https://image.tmdb.org/t/p/original"
                    url = baseImageURL + filePath

                    rjpeg = requests.get(url)
                    if rjpeg.status_code == 200:
                        sameLanguageImageFound = True
                        return  rjpeg.content ,len(backdropsJSON)
                else:
                        return  None,len(backdropsJSON)
            else:
                 resultJSON =r.json()
                 backdropsJSON = list(resultJSON.get("backdrops"))
                 return  None,len(backdropsJSON)

    def get_movie_from_id(self,movie_id):
        baseURL = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={self.TMDB_API_KEY}"

        r = requests.get(baseURL)

        if r.status_code == 200:
            return  r.json()

    def search_movie(self,query,language="en-US",page=1,include_adult=None,region=None,year=None,primary_release_year=None):
        search_Result = []

        URL = f"https://api.themoviedb.org/3/search/movie?api_key={self.TMDB_API_KEY}&language={language}&query={query}&page={page}&include_adult={include_adult}&region={region}&year={year}&primary_release_year={primary_release_year}"

        r = requests.get(URL)
        
        if r.status_code ==200:
            JSON = r.json()
            search_Result = list(JSON.get("results"))

        
        return search_Result
            
    def get_movie_credits(self,movie_id):

        BASE_URL = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={self.TMDB_API_KEY}"

        r = requests.get(BASE_URL)
        if r.status_code  == 200:
            JSON = r.json()

            cast = list( JSON.get("cast") )
            crew = list( JSON.get("crew") )
            
            if cast is not None:
                t1 = threading.Thread(target=self.start_people_threading , args=(cast,))
                
                t1.start()
            if crew is not None:
                t1 = threading.Thread(target=self.start_people_threading , args=(crew,))
                t1.start()
                             
            return cast ,crew
        else:
            return [],[]


    def start_people_threading(self,cast):
            try: 
                SYSTEM_PEOPLE_IDS =  views.SYSTEM_PEOPLE_ID
            except: 
                views.SYSTEM_PEOPLE_ID =   Database().get_all_people_ids()
            
            for person in cast:
                people_id = person.get("id")
                if people_id not in SYSTEM_PEOPLE_IDS:
                    self.add_people_to_db(people_id)



    def get_people_complete_details_from_id(self,person_id,language=None,append_to_response=None):
        try:
            
            BASE_URL = f"https://api.themoviedb.org/3/person/{person_id}?api_key={self.TMDB_API_KEY}&language={language}&append_to_response={append_to_response}"

            r = requests.get(BASE_URL)
            if r.status_code == 200:
                JSON = r.json()
                return JSON
        except :
            return None

    def add_people_to_db(self,people_id):
        myDB = Database()
        
        peopleJSON = self.get_people_complete_details_from_id(people_id)
        
        if peopleJSON:
            profile_path = peopleJSON.get("profile_path")
            IMAGE_BASE_URL = f"https://image.tmdb.org/t/p/original/{profile_path}"
            r = requests.get(IMAGE_BASE_URL)
            if r.status_code == 200:
                profile_picture = r.content
            else:
                profile_picture = None

            peopleJSON['profile_picture'] = profile_picture
            peopleJSON['profile_picture_path'] = profile_path
            myDB.add_people(peopleJSON,profile_picture)
           

    def get_similar_movies(self,movie_id,language=None,page=None):
        BASE_URL = f"https://api.themoviedb.org/3/movie/{movie_id}/similar?api_key={self.TMDB_API_KEY}&language={language}&page={page}"
           
           
        r = requests.get(BASE_URL)
        if r.status_code == 200:
            JSON = r.json()
            return JSON
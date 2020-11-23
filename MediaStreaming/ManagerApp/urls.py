from django.urls import path,include
from . import views,movies,upload_media,manage_sources

app_name = 'ManagerApp'


urlpatterns = [
   
    path('login/', views.loginPage,name="loginPage"),
    path('logout/', views.logoutUser,name="logoutUser"),

    path('', views.dashboard , name="dashboard"),
    
    path('movies/', movies.movie_dashboard , name="movie_dashboard"),
    path('movie/<int:movie_id>', movies.movie_details_page , name="movie_details"),
    path('movie/add_new', movies.add_new_movie , name="add_new_movie"),
    path('movie/add_new/search_result/<int:movie_id>', movies.view_tmdb_result , name="view_tmdb_result"),
    path('movie/add_movie_to_system/<int:movie_id>', movies.add_movie_to_system , name="add_movie_to_system"),
    path('movie/manage_sources', manage_sources.manage_sources_movies , name="manage_sources_movies"),
    path('movie/manage_sources/add_new_firebase_credentials', manage_sources.add_new_firebase_credentials , name="add_new_firebase_credentials"),


    
    path('upload_media/<int:media_id>', upload_media.upload_media_page , name="upload_media"),
    path('upload_media_firebase/<int:media_id>', upload_media.upload_media_firebase , name="upload_media_firebase"),


]



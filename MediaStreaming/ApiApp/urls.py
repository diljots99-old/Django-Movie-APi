from django.urls import path,include

from rest_framework import routers
from ApiApp import views,movies,users,people,torrent

from rest_framework.urlpatterns import format_suffix_patterns


# router = routers.DefaultRouter()

# router.register("movies",views.MovieApi)
# router.register("users",views.UserApi)
# router.urls
# urlpatterns = [
#     path('', include(router.urls)),
    
# ]
app_name = 'ApiApp'

urlpatterns = [
    path('movie/now_playing/', movies.get_now_playing_movies.as_view()),
    path('movie/top_rated/', movies.get_top_rated_movies.as_view()),
    path('movie/popular/', movies.get_popular_movies.as_view()),
    path('movie/new_releases/', movies.get_new_releases.as_view()),

    path('movie/poster/<int:movie_id>', movies.get_movie_poster.as_view(),name="movie_poster"),
    path('movie/poster_urls/<int:movie_id>', movies.get_movie_poster_urls.as_view()),
    path('movie/backdrop/<int:movie_id>', movies.get_movie_backdrop.as_view(),name="movie_backdrop"),
    path('movie/backdrop_urls/<int:movie_id>', movies.get_movie_backdrop_urls.as_view()),
    path('movie/details/<int:movie_id>', movies.get_complete_movie_details.as_view(),name='movie_details'),
    path('movie/credits/<int:movie_id>', movies.movie_credits.as_view()),
    path('movie/similar/<int:movie_id>', movies.similar_movies.as_view()),

    path('search/movie/', movies.search_movie.as_view()),


    path("user/",users.Users.as_view()),
    path("user/verify/",users.updateVerifiedUser.as_view()),

    path("user/history/<str:pk>",users.Users_History.as_view()),
    path("user/favourites/<str:pk>",users.Users_Favourites.as_view()),
    path("user/watchlist/<str:pk>",users.Users_Watchlist.as_view()),

    path('file/torrent/<int:torrent_id>',torrent.get_torrent_file.as_view()),


    path('people/profile_picture/<int:people_id>',people.get_people_profile_picture.as_view())


]

urlpatterns = format_suffix_patterns(urlpatterns)


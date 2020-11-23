from django.contrib import admin


# Register your models here.
from . import models

admin.site.register(models.Movies)
admin.site.register(models.Genres)
admin.site.register(models.Companies)
admin.site.register(models.People)
admin.site.register(models.PeopleAlsoKnownAs)
admin.site.register(models.Users)
admin.site.register(models.Torrents)
admin.site.register(models.ImagesBackdrops)
admin.site.register(models.ImagesPosters)
admin.site.register(models.MoviesToGenres)
admin.site.register(models.MoviesToTorrents)
admin.site.register(models.MoviesProductionCompanies)
admin.site.register(models.SourceGoogleDrive)

admin.site.register(models.UserWatchlist)
admin.site.register(models.UserHistory)
admin.site.register(models.UserFavourites)



''' admin.site.register(models.Departments)
admin.site.register(models.DeptEmp)
admin.site.register(models.DeptManager)
admin.site.register(models.Titles) '''
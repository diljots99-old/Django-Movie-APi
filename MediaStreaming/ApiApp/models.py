# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Companies(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.TextField(blank=True, null=True)
    headquarters = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    origin_country = models.CharField(max_length=10, blank=True, null=True)
    parent_company = models.CharField(max_length=50, blank=True, null=True)
    logo = models.TextField(blank=True, null=True)
    homepage = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'companies'


class Genres(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'genres'


class ImagesBackdrops(models.Model):
    backref_id = models.IntegerField(blank=True, null=True)
    image_category = models.CharField(max_length=10)
    image_data = models.TextField()
    aspect_ratio = models.FloatField(blank=True, null=True)
    heigth = models.FloatField(blank=True, null=True)
    width = models.FloatField(blank=True, null=True)
    iso_639_1 = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'images_backdrops'


class ImagesPosters(models.Model):
    backref_id = models.IntegerField(blank=True, null=True)
    image_category = models.CharField(max_length=10)
    image_data = models.TextField()
    aspect_ratio = models.FloatField(blank=True, null=True)
    heigth = models.FloatField(blank=True, null=True)
    width = models.FloatField(blank=True, null=True)
    iso_639_1 = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'images_posters'


class Movies(models.Model):
    
    adult = models.BooleanField(blank=True, null=True)
    id = models.IntegerField(primary_key=True)
    imdb_id = models.CharField(max_length=10, blank=True, null=True)
    original_language = models.CharField(max_length=10, blank=True, null=True)
    original_title = models.CharField(max_length=200, blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    runtime = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    tagline = models.TextField(blank=True, null=True)
    date_created = models.DateField(blank=True, null=True)
    date_updated = models.DateField(blank=True, null=True)
    streamable = models.BooleanField(blank=True, null=True)
    torrent = models.BooleanField(blank=True, null=True)
    vote_average = models.FloatField(blank=True, null=True)
    vote_count = models.IntegerField(blank=True, null=True)
    popularity = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movies'


class MoviesProductionCompanies(models.Model):
    movie = models.ForeignKey(Movies, models.DO_NOTHING)
    company = models.ForeignKey(Companies, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'movies_production_companies'


class MoviesToBackdrops(models.Model):
    movie = models.ForeignKey(Movies, models.DO_NOTHING, blank=True, null=True)
    backrop = models.ForeignKey(ImagesBackdrops, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movies_to_backdrops'


class MoviesToGenres(models.Model):
    movie = models.ForeignKey(Movies, models.DO_NOTHING)
    genre = models.ForeignKey(Genres, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'movies_to_genres'


class MoviesToPosters(models.Model):
    movie = models.ForeignKey(Movies, models.DO_NOTHING, blank=True, null=True)
    poster = models.ForeignKey(ImagesPosters, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movies_to_posters'


class MoviesToTorrents(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movies, models.DO_NOTHING)
    torrent = models.ForeignKey('Torrents', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'movies_to_torrents'


class People(models.Model):
    id = models.IntegerField(primary_key=True)
    birthday = models.DateField(blank=True, null=True)
    known_for_department = models.CharField(max_length=200, blank=True, null=True)
    death_day = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True)
    popularity = models.FloatField(blank=True, null=True)
    imdb_id = models.CharField(max_length=100, blank=True, null=True)
    homepage = models.CharField(max_length=100, blank=True, null=True)
    place_of_birth = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.BinaryField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    adult = models.BooleanField(blank=True, null=True)
    profile_picture_path = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people'


class PeopleAlsoKnownAs(models.Model):
    name = models.CharField(max_length=100)
    people = models.ForeignKey(People, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people_also_known_as'


class SourceGoogleDrive(models.Model):
    quality = models.CharField(max_length=100, blank=True, null=True)
    backref_id = models.IntegerField()
    size_bytes = models.IntegerField(blank=True, null=True)
    preview_url = models.CharField(max_length=200)
    sharing_url = models.CharField(max_length=200)
    drive_file_id = models.CharField(max_length=100)
    path = models.CharField(max_length=100, blank=True, null=True)
    drive_folder_id = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    filename = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'source_google_drive'


class Torrents(models.Model):
    url = models.TextField(blank=True, null=True)
    quality = models.CharField(max_length=15, blank=True, null=True)
    date_uploaded = models.DateField(blank=True, null=True)
    seeds = models.IntegerField(blank=True, null=True)
    peers = models.IntegerField(blank=True, null=True)
    size = models.CharField(max_length=20, blank=True, null=True)
    magent_url = models.TextField(blank=True, null=True)
    hash = models.TextField(blank=True, null=True)
    torrent_file = models.BinaryField(blank=True, null=True)
    torrent_source = models.CharField(max_length=20, blank=True, null=True)
    source_id = models.IntegerField(blank=True, null=True)
    size_bytes = models.IntegerField(blank=True, null=True)
    torrent_category = models.TextField(blank=True, null=True)
    backref_id = models.IntegerField(blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'torrents'


class Users(models.Model):
    uid = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    full_phone_number = models.CharField(max_length=200, blank=True, null=True)
    profile_picture = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class UserFavourites(models.Model):
    uid = models.ForeignKey('Users', models.DO_NOTHING, db_column='uid')
    type = models.CharField(max_length=100)
    backref_id = models.IntegerField()
    date_created = models.DateTimeField()
    last_accessed = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user__favourites'


class UserHistory(models.Model):
    uid = models.ForeignKey('Users', models.DO_NOTHING, db_column='uid')
    type = models.CharField(max_length=100)
    backref_id = models.IntegerField()
    date_created = models.DateTimeField()
    last_accessed = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user__history'


class UserWatchlist(models.Model):
    uid = models.ForeignKey('Users', models.DO_NOTHING, db_column='uid')
    type = models.CharField(max_length=100)
    backref_id = models.IntegerField()
    date_created = models.DateTimeField()
    last_accessed = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user__watchlist'

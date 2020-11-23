# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


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


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class FirebaseCredentials(models.Model):
    type = models.TextField()
    project_id = models.TextField()
    private_key_id = models.TextField()
    private_key = models.TextField()
    client_email = models.TextField()
    client_id = models.TextField()
    auth_uri = models.TextField()
    token_uri = models.TextField()
    auth_provider_x509_cert_url = models.TextField()
    client_x509_cert_url = models.TextField()
    owner_email = models.CharField(max_length=2000)

    class Meta:
        managed = False
        db_table = 'firebase__credentials'


class FirebaseMovies(models.Model):
    filename = models.CharField(max_length=200)
    file_path = models.CharField(max_length=1000)
    owner_email = models.CharField(max_length=2000)
    credentials = models.ForeignKey(FirebaseCredentials, models.DO_NOTHING, db_column='credentials')
    movie = models.ForeignKey('Movies', models.DO_NOTHING)
    quality = models.CharField(db_column='Quality', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'firebase__movies'


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
    adult = models.IntegerField(blank=True, null=True)
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
    streamable = models.IntegerField()
    torrent = models.IntegerField()
    vote_average = models.FloatField(blank=True, null=True)
    vote_count = models.IntegerField(blank=True, null=True)
    popularity = models.FloatField(blank=True, null=True)
    firbase_storage = models.IntegerField()

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
    profile_picture = models.TextField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    adult = models.IntegerField(blank=True, null=True)
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
    torrent_file = models.TextField(blank=True, null=True)
    torrent_source = models.CharField(max_length=20, blank=True, null=True)
    source_id = models.IntegerField(blank=True, null=True)
    size_bytes = models.IntegerField(blank=True, null=True)
    torrent_category = models.TextField(blank=True, null=True)
    backref_id = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'torrents'


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


class Users(models.Model):
    uid = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    full_phone_number = models.CharField(max_length=200, blank=True, null=True)
    profile_picture = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'

from rest_framework import serializers

from .models import *

class MoviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = "__all__"

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"

class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = "__all__"
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . import forms ,models,database

from .external_apis import Tmdb_api

import datetime

from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

from django.contrib import messages



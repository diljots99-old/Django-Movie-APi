from django import forms
from .models import SourceGoogleDrive,FirebaseMovies,FirebaseCredentials

from django.core.validators import EmailValidator

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control form-control-user","id":"exampleInputEmail",'aria-describedby':"emailHelp",
                                                'placeholder':"Username or Email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control form-control-user" ,"id":"exampleInputPassword", "placeholder":"Password"}))

    remember_me = forms.BooleanField(initial="False",label="Remember Me",required=False, widget=forms.CheckboxInput(attrs={"class":"custom-control-input" , "id":"customCheck" }))


class GoogleDriveSourceForm(forms.ModelForm):
    class Meta:
        model = SourceGoogleDrive
        fields = '__all__'


class FirebaseCredentialsForm(forms.Form):
    serviceAccount = forms.CharField(label="Service Account JSON",required= True,widget=forms.Textarea(attrs={"class":"form-control form-control-user","id":"exampleInputEmail",'aria-describedby':"emailHelp",
                                                'placeholder':"Paste Service Account JSON Here"}))
    owner_email = forms.EmailField(required =True,widget=forms.EmailInput(attrs={"class":"form-control form-control-user" ,"id":"exampleInputPassword", "placeholder":"Email"}),validators=[EmailValidator])

    
class FirebaseMoviesForm(forms.ModelForm):
    class Meta:
        model = FirebaseMovies
        fields = '__all__'
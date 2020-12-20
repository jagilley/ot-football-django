from django import forms
from django.db import models
from django.forms import ModelForm
from .models import UserExt, League

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    your_email = forms.EmailField()
    league_code = forms.CharField(label="League Code", max_length=10)

class JoinLeagueForm(forms.Form):
    username = forms.CharField(label="Username", max_length=30)
    league_code = forms.CharField(label="League Code", max_length=10)

"""
class LeagueCreation(forms.Form):
    league_name = forms.CharField(label="League Name", max_length=50, default="defaultname")
"""
class LeagueModelForm(ModelForm):
    class Meta:
        model = League
        fields = ["league_name", "publicly_joinable"]

class UserModelForm(ModelForm):
    class Meta:
        model = UserExt
        fields = ["name", "email", "league_code"]

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
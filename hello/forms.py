from django import forms
from django.db import models
from django.forms import ModelForm
from .models import User, League

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    your_email = forms.EmailField()
    league_code = forms.CharField(label="League Code", max_length=10)
"""
class LeagueCreation(forms.Form):
    league_name = forms.CharField(label="League Name", max_length=50, default="defaultname")
"""
class LeagueModelForm(ModelForm):
    class Meta:
        model = League
        fields = ["league_name"]

class UserModelForm(ModelForm):
    class Meta:
        model = User
        fields = ["name", "email", "league_code"]
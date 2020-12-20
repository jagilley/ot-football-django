from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)

class League(models.Model):
    league_name = models.CharField(default="defaultname", max_length=50)
    league_code = models.CharField(default="0000", max_length=10)
    publicly_joinable = models.BooleanField(default=False)

#default_league = League()
#default_league.save()

"""
class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=40)
    league_code = models.CharField(max_length=10, default="0000")
    league_model = models.ForeignKey(League, on_delete=models.CASCADE)
    wins = models.IntegerField()
    losses = models.IntegerField()
    total_points = models.FloatField()
"""
class UserExt(models.Model):
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=15, default="")
    email = models.EmailField()
    team_name = models.CharField(max_length=40, default="")
    league_code = models.CharField(max_length=10, default="0000")
    #league_model = models.ForeignKey(League, on_delete=models.CASCADE)
    wins = models.IntegerField()
    losses = models.IntegerField()
    total_points = models.FloatField()

class UserProfile(models.Model):
    usr = models.OneToOneField(User, on_delete=models.CASCADE)
    usrname = models.CharField(max_length=40, default="")
    team_name = models.CharField(max_length=40, default="")
    leagues = models.ManyToManyField(League)
    wins = models.IntegerField()
    losses = models.IntegerField()
    total_points = models.FloatField()
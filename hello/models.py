from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)

class League(models.Model):
    league_name = models.CharField(default="defaultname", max_length=50)
    league_code = models.CharField(default="0000", max_length=10)

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
class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    league_code = models.CharField(max_length=10, default="0000")
    league_model = models.ForeignKey(League, on_delete=models.CASCADE, default=1)
    wins = models.IntegerField()
    losses = models.IntegerField()
    total_points = models.FloatField()
from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)

class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=40)
    wins = models.IntegerField()
    losses = models.IntegerField()
    total_points = models.FloatField()
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests
from .models import Greeting
import random

# Create your views here.
def index(request):
    #r = requests.get('http://httpbin.org/status/418')
    #template = loader.get_template('templates/base.html')
    return render(request, "templates/base.html")


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})

def grid(request):
    scores = [round(random.uniform(0,20),2) for i in range(8)]
    total = sum(scores)
    return render(request, "grid.html", {"scores": scores, "total": total})
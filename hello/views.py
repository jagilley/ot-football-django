from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import requests
import string
import django
from .models import Greeting, League, User
from .forms import *
import random

# Create your views here.
def index(request):
    #r = requests.get('http://httpbin.org/status/418')
    #template = loader.get_template('templates/base.html')
    return render(request, "cover.html")


def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request, "db.html", {"greetings": greetings})

def register(request):
    return render(request, "register.html")

def process_reg(request):
    print(request)
    return render(request, "register.html")

def grid(request):
    my_user = User(name="Jasper Gilley", email="myemail@gmail.com")
    my_name = my_user.name
    scores = [round(random.uniform(0,20),2) for i in range(8)]
    total = round(sum(scores),2)
    return render(request, "grid.html", {"scores": scores, "total": total, "name": my_name})

def leaderboard(request):
    userz = User.objects.all()
    return render(request, "users.html", {"leader_users": userz})

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            all_leagues = League.objects.filter(league_code=form.cleaned_data['league_code'])
            if len(all_leagues) == 1:
                my_league = all_leagues[0]
            elif len(all_leagues) == 0:
                print("No league with this code")
            elif len(all_leagues) > 1:
                print("Multiple leagues with league code, choosing first")
                my_league = all_leagues[0]
            new_user = User(
                name=form.cleaned_data['your_name'],
                email=form.cleaned_data['your_email'],
                league_code=my_league,
                wins=0,
                losses=0,
                total_points=0.0
            )
            new_user.save()
            return HttpResponseRedirect('/thanks/')
    else:
        form = NameForm()
        return render(request, "name.html", {"form": form})

def create_league(request):
    if request.method == "POST":
        random_4_code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        form = LeagueModelForm(request.POST)
        if form.is_valid():
            new_league = form.save(commit=False)
            new_league.league_code = random_4_code
            new_league.save()
    else:
        form = LeagueModelForm()
    return render(request, 'create_league.html', {'form': form})
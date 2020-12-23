from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import requests
import string
import django
from .models import Greeting, League, UserExt, UserProfile, Team
from .forms import *
import random
import itertools
from .scores import player_scores_dummy
import pandas as pd
from glob import glob
from .equiv_pos import equiv_pos

def transpose(a_list):
    return list(map(list, itertools.zip_longest(*a_list, fillvalue=None)))

# Create your views here.
def index(request):
    return render(request, "cover.html")

def register(request):
    return render(request, "register.html")

def process_reg(request):
    print(request)
    return render(request, "register.html")

def grid(request):
    my_user = UserExt(name="Jasper Gilley", email="myemail@gmail.com")
    my_name = my_user.name
    scores = [round(random.uniform(0,20),2) for i in range(8)]
    total = round(sum(scores),2)
    return render(request, "grid.html", {"scores": scores, "total": total, "name": my_name})

def leaderboard(request):
    userz = UserExt.objects.all()
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
            new_user = UserExt(
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

def league_page(request, league_code="foobar"):
    try:
        my_league = League.objects.get(league_code=league_code)
    except IndexError:
        raise AssertionError("League code not found")
    league_profiles = [usr.usrname for usr in UserProfile.objects.filter(leagues=my_league)]
    return render(request, "league_page.html", {
        "header_bold": f"{my_league.league_name} - League Standings",
        "header_reg": (f"League code {my_league.league_code}, ") + ("publicly joinable" if my_league.publicly_joinable else "not publicly joinable"),
        "header_reg2": "League members: " + " ".join(league_profiles),
        "grid_items": [
            list(range(3)),
            list(range(3))
        ]
    })

def team_page(request, league_code="foobar", username="fobr"):
    my_user = request.user
    my_profile = UserProfile.objects.get(usr=my_user)
    try:
        my_team = Team.objects.get(league_code=league_code, username=username)
    except:
        #raise AssertionError("Team with this league code / user not found")
        my_team = Team(
            team_name="Fighting 4 Percent Mexicans",
            user=my_profile,
            league=League.objects.get(league_code=league_code)
        )
    """
    df = pd.DataFrame(columns=["Name", "Number", "Position", "Height", "Weight", "Age", "Exp", "College"])
    for thingythings in glob("hello/static/csv/*.csv"):
        df2 = pd.read_csv(thingythings)
        df2.columns = ["Name", "Number", "Position", "Height", "Weight", "Age", "Exp", "College"]
        df = df.append(df2)
    #print(random.choice(df[df["Position"] == "RB"]["Name"].tolist()))
    """
    df = pd.read_csv("hello/static/csv/all.csv")
    for k,v in my_team.players.items():
        try:
            my_team.players.update({
                k: random.choice(
                    df[(df["Position"].isin(equiv_pos[k]))]["Name"].tolist()
                )
            })
        except KeyError:
            print(k, equiv_pos[k])
        except IndexError:
            pass

    my_team.save()
    round_number = 1
    players_list = [[k, v, player_scores_dummy(v, round_number)] for k,v in my_team.players.items()]
    return render(request, "league_page.html", {
        "header_bold": (my_team.team_name + " - Team Points"),
        "header_reg": "More stuff here",
        "grid_items": players_list
    })

def public_leagues(request):
    all_public_leagues = League.objects.filter(publicly_joinable=True)
    data = [[leeg.league_name, leeg.league_code] for leeg in all_public_leagues]
    return render(request, "league_page.html", {
        "header_bold": "All Public Leagues",
        "header_reg": "",
        "grid_items": data
    })

def my_leagues(request):
    my_user = request.user
    my_profile = UserProfile.objects.get(usr=my_user)
    my_leagues = [[leeg.league_name, leeg.league_code] for leeg in my_profile.leagues.all()]
    return render(request, "league_page.html", {
        "header_bold": "My Leagues",
        "header_reg": "Leagues appear in order of joining",
        "grid_items": my_leagues
    })

from django.contrib.auth import login, authenticate
from hello.forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            profile = UserProfile(
                usr=user,
                usrname=username,
                wins=0,
                losses=0,
                total_points=0.0
            )
            profile.save()
            return redirect("/")
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def join_league(request):
    if request.method == "POST":
        form = JoinLeagueForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            code = form.cleaned_data['league_code']
            this_league = League.objects.get(league_code=code)
            user_obj = User.objects.get(username=username)
            profile = UserProfile.objects.get(usr=user_obj)
            profile.leagues.add(this_league)
            profile.save()
    else:
        form = JoinLeagueForm()
    return render(request, "join_league.html", {"form": form})
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
    UserProfiles = UserProfile.objects.filter(leagues=my_league)
    league_usrnames = [usr.usrname for usr in UserProfiles]
    league_standings = [[usr.usrname, Team.objects.get(user=usr, league=my_league).team_name, f"{usr.wins}-{usr.losses}", usr.total_points] for usr in UserProfiles]
    return render(request, "league_page2.html", {
        "header_bold": f"{my_league.league_name} - League Standings",
        "header_reg": (f"League code {my_league.league_code}, ") + ("publicly joinable, " if my_league.publicly_joinable else "not publicly joinable, ") + "draft has " + ("already" if my_league.already_drafted else "not") + " taken place.",
        "header_reg2": "League members: " + ", ".join(league_usrnames),
        "table_headers": ["Username", "Team Name", "Record", "Total Points", "Team Page"],
        "grid_items": league_standings,
        "leegcode": my_league.league_code
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
        "table_headers": ["League Name", "League Code"],
        "grid_items": data
    })

def my_leagues(request):
    my_user = request.user
    my_profile = UserProfile.objects.get(usr=my_user)
    my_leagues = [[leeg.league_name, leeg.league_code, ] for leeg in my_profile.leagues.all()]
    return render(request, "my_leagues2.html", {
        "header_bold": "My Leagues",
        "header_reg": "Leagues appear in order of joining",
        "table_headers": ["League Name", "League Code", "League Page"],
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
            my_user = request.user
            my_profile = UserProfile.objects.get(usr=my_user)
            #username = form.cleaned_data['username']
            code = form.cleaned_data['league_code']
            team_name = form.cleaned_data["team_name"]
            this_league = League.objects.get(league_code=code)
            #user_obj = User.objects.get(username=username)
            #profile = UserProfile.objects.get(usr=user_obj)
            my_profile.leagues.add(this_league)
            this_team = Team(
                user=my_profile,
                username=my_profile.usrname,
                league=this_league,
                league_code=code,
                team_name=team_name
            )
            my_profile.save()
            this_team.save()
    else:
        form = JoinLeagueForm()
    return render(request, "join_league.html", {"form": form})

def draft(request, league_code="foobar"):
    df = pd.read_csv("hello/static/csv/all.csv")
    return render(request, "draft.html", {
        "header_bold": "Draft",
        "table_headers": ["Name", "Number", "Position", "Height", "Weight", "Age", "Exp", "College"],
        "grid_items": df.to_numpy().tolist()
    })
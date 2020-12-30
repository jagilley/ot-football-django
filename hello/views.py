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
import json
from .equiv_pos import equiv_pos
from datetime import datetime, timedelta
import copy

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
        my_user = request.user
        try:
            defuser = User.objects.create_user("defaultuser")
            defuser.save()
        except:
            pass
        random_4_code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        form = LeagueModelForm(request.POST)
        if form.is_valid():
            new_league = form.save(commit=False)
            new_league.league_code = random_4_code
            new_league.creator = my_user
            new_league.save()

            # add user to league automatically

            my_profile = UserProfile.objects.get(usr=my_user)
            this_league = League.objects.get(league_code=random_4_code)
            my_profile.leagues.add(this_league)
            this_team = Team(
                user=my_profile,
                username=my_profile.usrname,
                league=this_league,
                league_code=random_4_code,
                #team_name=f"{this_league.league_name} Commissioner"
                team_name=random.choice([
                    "Supreme Leader",
                    "Head Honcho",
                    "Eternal Commissioner",
                    "Benevolent Dictator For Life",
                    "His/Her/Their Excellency",
                    "El Generalissimo",
                    "Chief Minister of Football",
                    "5 Star General Manager",
                    "Goodell's Second Coming"
                ])
            )
            my_profile.save()
            this_team.save()
            return HttpResponseRedirect(f"/league/{random_4_code}")
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
        "header_reg2": "League members: " + ", ".join(league_usrnames) + ".",
        "table_headers": ["Username", "Team Name", "Record", "Total Points", "Team Page", "Matchup Page"],
        "grid_items": league_standings,
        "leegcode": my_league.league_code,
        "this_league": my_league,
        "league_member_count": len(UserProfiles)
    })

def league_matchups(request, league_code="foobar"):
    try:
        my_league = League.objects.get(league_code=league_code)
    except IndexError:
        raise AssertionError("League code not found")
    return render(request, "league_page.html", {
        "header_bold": f"{my_league.league_name} - League Matchups",
        "grid_items": list(my_league.matchups.values())
    })

def team_page(request, league_code="foobar", username="fobr"):
    my_user = request.user
    my_profile = UserProfile.objects.get(usr=my_user)
    try:
        my_team = Team.objects.get(league_code=league_code, username=username)
    except:
        #raise AssertionError("Team with this league code / user not found")
        my_team = Team(
            team_name="Auto-created team",
            user=my_profile,
            league=League.objects.get(league_code=league_code)
        )
    if my_team.players["QB"] == "" and my_team.players["RB1"] == "" and my_team.players["WR1"] == "":
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

def matchup(request, league_code="foobar", username="foobar", week=1):
    my_user = request.user
    my_profile = UserProfile.objects.get(usr=my_user)
    try:
        my_team = Team.objects.get(league_code=league_code, username=username)
    except:
        #raise AssertionError("Team with this league code / user not found")
        my_team = Team(
            team_name="Auto-created team",
            user=my_profile,
            league=League.objects.get(league_code=league_code)
        )
    
    if my_team.players["QB"] == "" and my_team.players["RB1"] == "" and my_team.players["WR1"] == "":
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
    return render(request, "matchup.html", {
        "header_bold": (my_team.team_name + f" - Matchup Week {week}"),
        "grid_items": players_list
    })

def public_leagues(request):
    all_public_leagues = League.objects.filter(publicly_joinable=True)
    data = [[leeg.league_name, leeg.league_code] for leeg in all_public_leagues]
    return render(request, "league_page.html", {
        "header_bold": "All Public Leagues",
        "header_reg": "Sign up to join",
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
            return HttpResponseRedirect(f"/league/{code}")
    else:
        form = JoinLeagueForm()
    return render(request, "join_league.html", {"form": form})

from pytz import timezone

def draft(request, league_code="foobar"):
    df = pd.read_csv("hello/static/csv/all.csv")

    # ALERT - this should be removed (?)
    my_league = League.objects.get(league_code=league_code)
    eastern = timezone('US/Eastern')
    my_league.draft_started_at = datetime.now(tz=eastern)

    my_league.matchups = {}
    league_participants = [team.username for team in Team.objects.filter(league_code=league_code)]
    random.shuffle(league_participants)
    #my_league.draft_order = " ".join(league_participants)
    my_league.draft_order_list = league_participants
    my_league.drafting_player_un = league_participants[0]
    """
    for i in range(1,4):
        for player in league_participants:
            my_league.matchups[f"week{i}"][player] = """
    for i in range(1,4):
        my_league.matchups[f"week{i}"] = {}
        already_scheduled = []
        for player in league_participants:
            if player in already_scheduled:
                #print("skipping", player, "already scheduled")
                continue
            non_player = copy.deepcopy(league_participants)
            non_player.remove(player)
            if i == 2:
                last_week_opp = my_league.matchups["week1"][player]
                if last_week_opp in non_player:
                    non_player.remove(last_week_opp)
            if i == 3:
                last_week_opp1 = my_league.matchups["week1"][player]
                last_week_opp2 = my_league.matchups["week2"][player]
                if last_week_opp1 in non_player:
                    non_player.remove(last_week_opp1)
                if last_week_opp2 in non_player:
                    non_player.remove(last_week_opp2)
            non_player = [j for j in non_player if j not in already_scheduled]

            my_opponent = random.choice(non_player)
            my_league.matchups[f"week{i}"][player] = my_opponent
            my_league.matchups[f"week{i}"][my_opponent] = player
            #print("week", i, "-", player, "playing", my_opponent)
            already_scheduled.append(player)
            already_scheduled.append(my_opponent)
            #print("already sch is", already_scheduled)
    """
    # the 1 seed always plays the 234 seeds
    for i in range(1,4):
        my_league.matchups["week"][league_participants[0]] = league_participants[i]
    
    for nth_participant in league_participants[1:]:
        for i in range(1,4):
            week_matchups = []
            index_adjust = i - 1
            pcpt_cnt = len(league_participants)
            
            for iter_count, participant in enumerate(league_participants):
                week_matchups.append(
                    [league_participants[(iter_count + index_adjust) % pcpt_cnt], league_participants[(iter_count + 1 + index_adjust) % pcpt_cnt]]
                )
            
            my_league.matchups[][nth_participant]
            
            for pcpt1 in league_participants:
                for pcpt2 in league_participants:
                    if pcpt1 != pcpt2:
                        week_matchups.append([pcpt1, pcpt2])
            
        my_league.matchups["week"] = week_matchups
    """
    my_league.save()

    return render(request, "draft.html", {
        "header_bold": "Draft",
        "header_reg": f"Started at {my_league.draft_started_at.strftime('%m/%d/%Y, %H:%M:%S')}",
        "header_reg2": f"Draft order is: {', '.join(my_league.draft_order_list)}",
        "table_headers": df.columns,
        "grid_items": df.to_numpy().tolist(),
        "leegcode": league_code
    })

from django.http import JsonResponse

def get_players(request):
    df = pd.read_csv("hello/static/csv/all.csv").fillna(0)
    return JsonResponse(df.to_dict("records"), safe=False)

def draft_player(request):
    my_user = request.user
    my_profile = UserProfile.objects.get(usr=my_user)
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        my_league = League.objects.get(league_code=request.headers["leaguecode"])
        if len(body_data) > 1:
            raise AssertionError("Can't draft more than 1 guy at a time")
        if my_user.username != my_league.drafting_player_un:
            raise AssertionError("Hey, you're not supposed to draft, asshole!")
        player_pos = body_data[0]["Position"]
        player_name = body_data[0]["Name"]
        my_team = Team.objects.get(
            user=my_profile,
            league_code=request.headers["leaguecode"]
        )
        my_team.players[player_pos] = player_name
        my_team.save()
        # Draft management
        my_league.draft_history.append(f"{my_user.username} has drafted {player_pos} {player_name} to {my_team.team_name}")
        do_list = my_league.draft_order_list
        cdlist = do_list.pop(0)
        do_list.append(cdlist)
        my_league.drafting_player_un = do_list[0]
        my_league.draft_started_at = datetime.now(tz=timezone('US/Eastern'))
        my_league.save()
        return HttpResponse(status=205)

def draft_timeout(league_code="foobar", usrname="usrname"):
    my_league = League.objects.get(league_code=league_code)
    my_league.draft_history.append(f"{usrname}'s draft slot timed out, going to next player")
    do_list = my_league.draft_order_list
    do_list.append(do_list.pop(0))
    my_league.drafting_player_un = do_list[0]
    my_league.draft_started_at = datetime.now(tz=timezone('US/Eastern'))
    my_league.save()
    return HttpResponse(status=205)

def draft_history(request, league_code="foobar"):
    this_league = League.objects.get(league_code=league_code)
    df = pd.DataFrame(this_league.draft_history, columns=["Draft History"])
    return JsonResponse(df.to_dict("records"), safe=False)

def draft_info(request):
    this_league = League.objects.get(league_code=request.headers["leaguecode"])
    start_time = this_league.draft_started_at
    eastern = timezone('US/Eastern')
    now = datetime.now(tz=eastern)
    delta = now - start_time
    if delta > timedelta(minutes=2):
        draft_timeout(league_code=request.headers["leaguecode"], usrname=request.user.username)
    deltastr = str(delta).split(".")[0][3:]
    return JsonResponse({
        "draft_time": deltastr,
        "drafter": this_league.draft_order_list[0]
    }, safe=False)
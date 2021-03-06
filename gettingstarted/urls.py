from django.urls import path, include

from django.contrib import admin

admin.autodiscover()

import hello.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", hello.views.index, name="cover"),
    path("grid/", hello.views.grid, name="grid"),
    path("name/", hello.views.get_name, name="name"),
    path("leaderboard/", hello.views.leaderboard, name="leaderboard"),
    path("create_league/", hello.views.create_league, name="create_league"),
    path("admin/", admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path("league/<slug:league_code>/", hello.views.league_page, name="leaguepage"),
    path("league/<slug:league_code>/draft/", hello.views.draft, name="draft"),
    path("league/<slug:league_code>/draft/history", hello.views.draft_history, name="draft_history"),
    path("draft_info/", hello.views.draft_info, name="draft_info"),
    path("get_players/", hello.views.get_players, name="get_players"),
    path("draft_player/", hello.views.draft_player, name="draft_player"),
    path("signup/", hello.views.signup, name="signup"),
    path("public/", hello.views.public_leagues, name="public"),
    path("join_league/", hello.views.join_league, name="join_league"),
    path("my_leagues/", hello.views.my_leagues, name="my_leagues"),
    path("league/<slug:league_code>/team/<slug:username>/", hello.views.team_page, name="team_page"),
    path("league/<slug:league_code>/matchup/<slug:username>/<int:week>/", hello.views.matchup, name="matchup"),
    path("league/<slug:league_code>/matchups/", hello.views.league_matchups, name="matchups"),
    path("faq/", hello.views.faq, name="faq"),
    path("contact/", hello.views.contact, name="contact")
]
"""
    ^ this includes:
    accounts/login/ [name='login']
    accounts/logout/ [name='logout']
    accounts/password_change/ [name='password_change']
    accounts/password_change/done/ [name='password_change_done']
    accounts/password_reset/ [name='password_reset']
    accounts/password_reset/done/ [name='password_reset_done']
    accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
    accounts/reset/done/ [name='password_reset_complete']
"""
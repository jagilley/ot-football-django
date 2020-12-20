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
    path("db/", hello.views.db, name="db"),
    path("grid/", hello.views.grid, name="grid"),
    path("register/", hello.views.register, name="register"),
    path("register-me/", hello.views.process_reg, name="process_reg"),
    path("name/", hello.views.get_name, name="name"),
    path("leaderboard/", hello.views.leaderboard, name="leaderboard"),
    path("create_league/", hello.views.create_league, name="create_league"),
    path("admin/", admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path("league/<slug:league_code>/", hello.views.league_page),
    path("signup/", hello.views.signup, name="signup")
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
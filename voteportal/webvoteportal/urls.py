from django import views
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('home', views.home, name="home"),
    path('login', views.view_login, name="login"),
    path('contest', views.user_contest, name="contest"),
    path('vote', views.user_vote, name="vote"),
    path('logout', views.view_logout, name="logout"),
    path('register', views.register, name="register"),
    path('blockchain', views.mine_block, name="blockmine"),
    path('blockchaindata', views.offline_block, name="offlineblockchain" )
    ]
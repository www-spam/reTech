from django.urls import path

from . import views

urlpatterns = [
    path('0_waste', views.zerowaste, name='0_waste'),
    path('chatbot', views.chatbot, name='chatbot'),
    path('home_login', views.home_login, name='home_login'),
    path('home', views.home, name='home'),
    path('mini_game', views.mini_game, name='mini_game'),

    path('nephron', views.nephron, name='nephron'),
    path('recycling_center', views.recycling_center, name='recycling_center'),
    path('recycling_market', views.recycling_market, name='recycling_market'),

    path('member', views.member, name='member'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('community/',views.community, name='community'),
    path('new_post/',views.new_post, name="new_post"),
]
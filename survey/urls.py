from django.urls import path
from . import views

urlpatterns = [
    path('survey', views.survey, name="survey"),
    path('login_check', views.login_check, name="login_check"),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote')
]

app_name = 'survey'
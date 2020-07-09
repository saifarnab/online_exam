from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('papers', views.papers, name='papers'),
    path('createpaper', views.create_papers, name='createpaper'),
    path('createquestion', views.create_question, name='createquestion'),
    path('paperlist', views.papers_list, name='paperlist'),
    path('createuser', views.create_user, name='createuser'),
    path('logout', views.logout_session, name='logout')
]
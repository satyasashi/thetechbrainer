from django.urls import path, re_path
from . import views

app_name = "user"

urlpatterns = [
    path('', views.index, name="index"),
    re_path(r'^drafts/$', views.user_drafts, name="user_drafts"),
    re_path(r'^ajax/follow-author/$',  views.follow, name="follow_author"),
    path('interests/', views.user_interests, name="user_interests"),
    path('page-not-found', views.pagenotfound, name="pagenotfound"),
    path('dashboard/', views.user_dashboard, name="user_dashboard"),
    path('ajax/get-user-info/', views.get_user_information, name="get_user_information"),
]

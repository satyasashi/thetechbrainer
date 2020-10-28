from django.urls import path, re_path
from . import views

app_name = "user"

urlpatterns = [
    path('', views.index, name="index"),
    path('about-us/', views.about, name="about_us"),
    re_path(r'^drafts/$', views.user_drafts, name="user_drafts"),
    re_path(r'^ajax/follow-author/$',  views.follow, name="follow_author"),
    path('interests/', views.user_interests, name="user_interests"),
    path('page-not-found', views.pagenotfound, name="pagenotfound"),
    path('dashboard/', views.user_dashboard, name="user_dashboard"),
    path('ajax/get-user-info/', views.get_user_information, name="get_user_information"),
    path('ajax/unfollow-author/', views.unfollow_author, name="unfollow_author"),
    path('moderator-dashboard/', views.moderator_dashboard, name="moderator_dashboard"),
]

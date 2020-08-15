from django.urls import path, re_path
from . import views

app_name = "user"

urlpatterns = [
    path('', views.index, name="index"),
    re_path(r'^ajax/follow-author/$',  views.follow, name="follow_author"),
    path('interests/', views.user_interests, name="user_interests"),
]

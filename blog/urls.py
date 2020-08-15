from django.urls import path, re_path
from . import views

app_name = "blog"

urlpatterns = [
    path('search/', views.blog_search, name="blog_search"),
    re_path(r'ajax/bookmark/(?P<blog_slug>[\w\d-]+)$', views.bookmark_blogpost, name="bookmark_blogpost"),
    re_path(r'^(?P<slug>[\w\d-]+)/$', views.blog_detail, name="blog_detail"),
]

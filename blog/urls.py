from django.urls import path, re_path
from . import views

app_name = "blog"

urlpatterns = [
    path('search/', views.blog_search, name="blog_search"),
    path('categories/', views.get_categories, name="blog_categories"),
    re_path(r'^preview/(?P<blog_slug>[\w\d-]+)/$', views.preview_blog, name="preview_blog"),
    path('new-blog-post/', views.write_blog, name="write_blog"),
    re_path(r'ajax/bookmark/(?P<blog_slug>[\w\d-]+)$', views.bookmark_blogpost, name="bookmark_blogpost"),
    re_path(r'ajax/like/(?P<blog_slug>[\w\d-]+)$', views.like_blogpost, name="like_blogpost"),
    re_path(r'ajax/blog-request/(?P<category_id>[\d]+)$', views.blog_request, name="blog_request"),
    re_path(r'^(?P<slug>[\w\d-]+)/$', views.blog_detail, name="blog_detail"),
    re_path(r'^filter-by-category/(?P<category_slug>[\w\d-]+)$', views.filter_by_category, name="filter_by_category"),
    re_path(r'^filter-by-tag/(?P<tag_slug>[\w\d-]+)$', views.filter_by_tag, name="filter_by_tag"),
]

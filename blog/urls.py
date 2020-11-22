from django.urls import path, re_path
from . import views

app_name = "blog"

urlpatterns = [
    path('search/', views.blog_search, name="blog_search"),
    path('categories/', views.get_categories, name="blog_categories"),
    path('my-blogs/', views.my_blogs, name="my_blogs"),
    path('new-blog-post/', views.write_new_blog, name="write_new_blog"),
    path('new-blog-post-preview/', views.save_blog_and_show_preview, name="save_blog_and_show_preview"),
    # path('blog/submit-for-moderation/', views.submit_blog_for_moderation, name="submit_blog_for_moderation"),
    path('blog-tags/', views.blog_tags, name="blog_tags"),
    re_path(r'^edit-blog-post/(?P<id>[\d]+)/(?P<slug>[\w\d-]+)/$', views.edit_blog, name="edit_blog_post"),
    #
    re_path(r'ajax/bookmark/(?P<id>[\d]+)$', views.bookmark_blogpost, name="bookmark_blogpost"),
    re_path(r'ajax/like/(?P<id>[\d]+)$', views.like_blogpost, name="like_blogpost"),
    re_path(r'ajax/blog-request/(?P<category_id>[\d]+)$', views.blog_request, name="blog_request"),
    re_path(r'^ajax/submit-for-moderation-preview/$', views.submit_for_moderation, name="submit_for_moderation"),
    #
    re_path(r'^(?P<id>[\d]+)/(?P<slug>[\w\d-]+)/$', views.blog_detail, name="blog_detail"),
    re_path(r'^draft/(?P<id>[\d]+)/(?P<slug>[\w\d-]+)/$', views.draft_blog_detail, name="draft_blog_detail"),
    re_path(r'^awaiting-moderation/(?P<id>[\d]+)/(?P<slug>[\w\d-]+)/$', views.awaiting_moderation_blog_detail, name="awaiting_moderation"),
    re_path(r'^preview/(?P<id>[\d]+)/(?P<blog_slug>[\w\d-]+)/$', views.preview_blog, name="preview_blog"),
    # re_path(r'^preview/from-edit-blog/$', views.preview_from_edit_blog, name="preview_from_edit_blog"),
    #
    re_path(r'^filter-by-category/(?P<category_slug>[\w\d-]+)$', views.filter_by_category, name="filter_by_category"),
    # re_path(r'^filter-by-tag/(?P<slug>[\w\d-]+)$', views.filter_by_tag, name="filter_by_tag"),
    re_path(r'^filter-by-author/(?P<id>[\d]+)$', views.filter_by_author, name="filter_by_author"),
    #
    re_path(r'^accept-and-publish/blog/(?P<id>[\d]+)/$', views.accept_and_publish, name="accept_and_publish"),
]

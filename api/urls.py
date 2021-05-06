from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, re_path
from .views import PostList, PostDetail

app_name = "api"

urlpatterns = [
    path('', PostList.as_view(), name="api_bloglist"),
    path('post/<int:pk>/', PostDetail.as_view(), name="api_blogdetail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
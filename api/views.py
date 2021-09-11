from rest_framework import generics, permissions, viewsets
from blog.models import BlogPost
from .serializers import PostSerializer
from api.permissions import IsAuthorOrReadOnly, HasAuthorGroupOrReadOnly


# Create your views here.
class PostList(generics.ListCreateAPIView):
    """LIST of items or Create an item"""
    queryset = BlogPost.objects.filter(published=True)
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, HasAuthorGroupOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(blog_author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """Retreive specific item or Destroy specific item"""
    queryset = BlogPost.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly]

from rest_framework import serializers
from taggit_serializer.serializers import (
	TagListSerializerField,
	TaggitSerializer
	)
from django.contrib.auth.models import User
from blog.models import BlogPost

class PostSerializer(TaggitSerializer, serializers.HyperlinkedModelSerializer):
	blog_tags = TagListSerializerField()
	blog_author = serializers.ReadOnlyField(source="blog_author.username")
	url = serializers.HyperlinkedIdentityField(view_name="api:api_blogdetail")
	blog_category = serializers.ReadOnlyField(source="blog_category.category_name")
	published = serializers.ReadOnlyField() 

	class Meta:
		model = BlogPost
		fields = (
			'url',
			'blog_author', 
			'blog_title', 
			'blog_subtitle', 
			'banner_image', 
			'banner_image_source', 
			'blog_category', 
			'blog_tags',
			'published'
			)
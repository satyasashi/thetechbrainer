from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import BlogPost, Category


# class Test_Create_BlogPost(TestCase):
	
# 	@classmethod
# 	def setUpTestData(cls):
# 		dummy_user = User.objects.create_user(
# 			username='test_user1',
# 			password='Test@123'
# 			)

# 		dummy_category = Category.objects.create(
# 			category_name='Dummy',
# 			category_slug='dummy',
			
# 			)


# 		test_blog = BlogPost.objects.create(
# 			blog_author=dummy_user,
# 			blog_title='Testing Title',
# 			blog_subtitle='This is a subtitle from tests.py',
# 			banner_image_source='By dummy_user',
# 			content='Some basic content',
# 			blog_category=,
# 			blog_tags=
# 			)


# 		test_blog.blog_image = SimpleUploadedFile(
# 			name='oop-python.png', 
# 			content=open('', 'rb').read(), 
# 			content_type='image/jpeg'
# 			)
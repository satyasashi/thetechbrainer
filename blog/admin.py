from django.contrib import admin
from .models import Role, Category, BlogPost, Tag

# Register your models here.
admin.site.register(Role)
admin.site.register(Category)
admin.site.register(BlogPost)
admin.site.register(Tag)

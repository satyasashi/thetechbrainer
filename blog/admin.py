from django.contrib import admin
from .models import Role, Category, BlogPost

# Register your models here.
admin.site.register(Role)
admin.site.register(Category)
admin.site.register(BlogPost)

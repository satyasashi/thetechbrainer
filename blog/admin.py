from django.contrib import admin
from .models import Role, Category, BlogPost, BlogRequest, BlogTag


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('blog_author', 'blog_title', 'created_on')
    search_fields = ['blog_title']
    ordering = ['-created_on']
    list_filter = ['blog_author']
    date_hierarchy = 'created_on'


# Register your models here.
admin.site.register(Role)
admin.site.register(Category)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(BlogRequest)
admin.site.register(BlogTag)

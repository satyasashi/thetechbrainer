from django.db import models
from django.contrib.auth.models import User
from siteuser.models import SiteUser
from django.utils.text import slugify
from siteuser.utils import banner_path


class Role(models.Model):
    role_name = models.CharField(max_length=100)
    role_slug = models.SlugField(blank=True)

    class Meta:
        db_table = "role"

    def save(self, *args, **kwargs):
        if not self.id:
            # newly created object, so create slug.
            self.role_slug = slugify(self.role_name)
        super(Role, self).save(*args, **kwargs)

    def __str__(self):
        return self.role_name


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    category_slug = models.SlugField(blank=True)

    class Meta:
        db_table = "category"

    def save(self, *args, **kwargs):
        if not self.id:
            # newly created object, so create slug.
            self.category_slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name


class Tag(models.Model):
    tag_name = models.CharField(max_length=100)
    tag_slug = models.SlugField(blank=True)

    class Meta:
        db_table = "tag"

    def save(self, *args, **kwargs):
        if not self.id:
            # newly created object, so create slug.
            self.tag_slug = slugify(self.tag_name)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.tag_name


class BlogPost(models.Model):
    blog_author = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    blog_title = models.CharField(max_length=100, help_text="Keep titles short.")
    blog_subtitle = models.CharField(max_length=150, help_text="Short line for subtitle.")
    blog_slug = models.SlugField(blank=True, help_text="Slug will be automatically generated.")
    banner_image = models.ImageField(upload_to=banner_path)
    content = models.TextField()

    blog_category = models.ManyToManyField(Category)
    blog_tags = models.ManyToManyField(Tag)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "blog_post"

    def save(self, *args, **kwargs):
        if not self.id:
            # newly created object, so create slug.
            self.blog_slug = slugify(self.blog_title)
        super(BlogPost, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.blog_author.user.username)

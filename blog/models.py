from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from siteuser.models import SiteUser
from django.utils.text import slugify
from toolbelt.utils import (
    banner_path,
    category_img_path,
    get_category_img_thumbnail_path,
    get_user_directory_thumbnail_path,
    get_random_string
    )
from ckeditor_uploader.fields import RichTextUploadingField
from PIL import Image

import os
import uuid


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
    category_image = models.ImageField()
    category_line = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        db_table = "category"

    def save(self, *args, **kwargs):
        if not self.id:
            # newly created object, so create slug.
            self.category_slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

        # make thumbnail from original image.
        # img = Image.open(self.category_image)
        # img.thumbnail(settings.IMG_SMALL)  # result dimensions
        # img_thumbnail_path = get_category_img_thumbnail_path(self.category_name, self.category_image)
        # try:
        #     img.save(img_thumbnail_path)
        #     print("Image Thumbnail saved")
        # except FileNotFoundError:
        #     os.makedirs(settings.MEDIA_ROOT+"/category/"+self.category_name+"/thumbnails/")
        #     img.save(img_thumbnail_path)
        #     print("Created thumbnails folder.")

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
    blog_slug = models.SlugField(blank=True, max_length=500, help_text="Slug will be automatically generated.")
    banner_image = models.ImageField()
    banner_image_source = models.CharField(max_length=50, default="")
    content = RichTextUploadingField(blank=True, null=True)

    blog_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    blog_tags = models.ManyToManyField(Tag)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    moderator_accepted = models.BooleanField(default=False)
    draft = models.BooleanField(default=False)
    preview = models.BooleanField(default=False)
    submitted_for_moderation = models.BooleanField(default=False)
    published = models.BooleanField(default=False)

    class Meta:
        db_table = "blog_post"

    def filename(self):
        return os.path.basename(self.banner_image.name)

    """Modifying the default save() method to create slug from photo title"""
    def save(self, *args, **kwargs):
        if not self.id:
            # newly created object, so create slug.
            random_string = get_random_string(5)
            self.blog_slug = slugify(self.blog_title) + "-" + str(random_string)

        super(BlogPost, self).save(*args, **kwargs)
        # self.banner_image = self.banner_image.small()

        # make thumbnail from original image.
        img = Image.open(self.banner_image)
        img.thumbnail(settings.IMG_SMALL)  # result dimensions
        img_thumbnail_path = get_user_directory_thumbnail_path(self.blog_author.user.id, self.banner_image)
        try:
            img.save(img_thumbnail_path)
            print("Image Thumbnail saved")
        except FileNotFoundError:
            os.makedirs(settings.MEDIA_ROOT+"/user_{}/banners/thumbnails/".format(self.blog_author.user.id))
            img.save(img_thumbnail_path)
            print("Created thumbnails folder.")

    # def __str__(self):
    #     return self.blog_author


class BlogRequest(models.Model):
    siteuser = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    blog_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    requested_on = models.DateTimeField(auto_now_add=True)
    requested_again_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "blog_request"

    def __str__(self):
        return self.blog_category

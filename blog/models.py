from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase
from django.contrib.auth.models import User
from django.conf import settings
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


# Create your models here.
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


class MyCustomTag(TagBase):
    # ... fields here

    class Meta:
        verbose_name = "Custom Tag"
        verbose_name_plural = "Custom Tags"

    def __str__(self):
        return self.name


class BlogTag(GenericTaggedItemBase):
    # TaggedWhatever can also extend TaggedItemBase or a combination of
    # both TaggedItemBase and GenericTaggedItemBase. GenericTaggedItemBase
    # allows using the same tag for different kinds of objects, in this
    # example Food and Drink.

    # Here is where you provide your custom Tag class.
    tag = models.ForeignKey(
        MyCustomTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )

    def __str__(self):
        return self.tag.name


class BlogPost(models.Model):
    blog_author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_title = models.CharField(max_length=100, help_text="Keep titles short.")
    blog_subtitle = models.CharField(max_length=150, help_text="Short line for subtitle.")
    blog_slug = models.SlugField(blank=True, max_length=500, help_text="Slug will be automatically generated.")
    banner_image = models.ImageField(blank=True)
    banner_image_source = models.CharField(max_length=50, default="")
    content = RichTextUploadingField(blank=True, null=True)

    blog_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    blog_tags = TaggableManager(blank=True, through='BlogTag')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    moderator_accepted = models.BooleanField(default=False)
    draft = models.BooleanField(default=False)
    preview = models.BooleanField(default=False)
    submitted_for_moderation = models.BooleanField(default=False)
    published = models.BooleanField(default=False)

    class Meta:
        db_table = "blog_post"
        ordering = ['-id']
        unique_together = ("id", "blog_slug")

    def filename(self):
        return os.path.basename(self.banner_image.name)

    """Modifying the default save() method to create slug from photo title"""
    def save(self, *args, **kwargs):
        if not self.id:
            # newly created object, so create slug.
            # random_string = get_random_string(5)
            self.blog_slug = slugify(self.blog_title)

        super(BlogPost, self).save(*args, **kwargs)

        # make thumbnail from original image.
        img = Image.open(self.banner_image)
        img.thumbnail(settings.IMG_SMALL)  # result dimensions
        img_thumbnail_path = get_user_directory_thumbnail_path(self.blog_author.id, self.banner_image)
        try:
            img.save(img_thumbnail_path)
        except FileNotFoundError:
            os.makedirs(settings.MEDIA_ROOT+"/user_{}/banners/thumbnails/".format(self.blog_author.id))
            img.save(img_thumbnail_path)

    def __str__(self):
        return self.blog_title


class BlogRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    requested_on = models.DateTimeField(auto_now_add=True)
    requested_again_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "blog_request"

    def __str__(self):
        return self.blog_category.category_name

from django.db import models
from toolbelt.utils import use_directory_path
from django.contrib.auth.models import User


# Create your models here.
class SiteUser(models.Model):
    GENDER_CHOICES = (
        ('M', 'MALE'),
        ('F', 'FEMALE'),
        ('O', 'OTHER')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, blank=True, null=True, max_length=1)
    roles = models.ForeignKey('blog.Role', on_delete=models.CASCADE, null=True, blank=True, default=1)
    interests = models.ManyToManyField('blog.Category')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "site_user"

    def __str__(self):
        return self.user.username


class PersonalInformation(models.Model):
    siteuser = models.OneToOneField(SiteUser, on_delete=models.CASCADE)
    introduction = models.TextField()
    picture = models.ImageField(upload_to=use_directory_path, null=True, blank=True)
    interests = models.ManyToManyField('blog.Category')

    # Social media only to authors.
    facebook = models.URLField(null=True, blank=True)
    github = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    insta = models.URLField(null=True, blank=True)

    class Meta:
        db_table = "personal_information"

    def __str__(self):
        return self.siteuser.user.username


class UserLikes(models.Model):
    siteuser = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    blog = models.ForeignKey('blog.BlogPost', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = "user_likes"

    def __str__(self):
        return self.siteuser.user.username


class UserFollowing(models.Model):
    """Stores User(Viewer's) Follower list"""
    siteuser = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    following = models.ForeignKey(SiteUser, on_delete=models.CASCADE, related_name="following")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = "user_following"

    def __str__(self):
        return self.siteuser.user.username


class UserBookmarks(models.Model):
    """Stores User(Viewer's) Blog Bookmarks"""
    user = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    blog_post = models.ForeignKey('blog.BlogPost', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.user + "-" + self.blog_post

    class Meta:
        verbose_name = "UserBookmark"
        verbose_name_plural = "UserBookmarks"

    def __str__(self):
        return self.user.user.username

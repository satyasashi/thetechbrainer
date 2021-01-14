from django.db import models
from django.contrib.auth.models import User
from blog.models import BlogPost


# Create your models here.
class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'MALE'),
        ('F', 'FEMALE'),
        ('O', 'OTHER')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, blank=True, null=True, max_length=1)
    roles = models.ForeignKey('blog.Role', on_delete=models.CASCADE, null=True, blank=True)
    interests = models.ManyToManyField('blog.Category')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "profile"

    def __str__(self):
        return self.user.username


class PersonalInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    introduction = models.CharField(max_length=200)
    full_introduction = models.TextField(default="")
    picture = models.ImageField()
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
        return self.user.username


class UserLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey('blog.BlogPost', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = "user_likes"

    def __str__(self):
        return self.user


class UserFollowing(models.Model):
    """Stores User(Viewer's) Follower list"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = "user_following"

    def __str__(self):
        return self.user.username


class UserBookmarks(models.Model):
    """Stores User(Viewer's) Blog Bookmarks"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_post = models.ForeignKey('blog.BlogPost', on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = "UserBookmark"
        verbose_name_plural = "UserBookmarks"

    def __str__(self):
        return self.user


class Notifications(models.Model):
    """Stores User's Notifications"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    read = models.BooleanField(default=False)
    url = models.URLField()
    # blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    notify = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notify_author")
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return self.title

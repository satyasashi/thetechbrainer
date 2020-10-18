from django.conf import settings
import random
import string

def banner_path(instance, filename):
    return "user_{0}/banners/{1}".format(instance.blog_author.user.id, filename)


def category_img_path(instance, filename):
    return "category/{0}/{1}".format(instance.category_name, filename)


def get_category_img_thumbnail_path(category_name, img_name):
    img_name = img_name.name.split("/")[-1]
    thumbnail_path = settings.MEDIA_ROOT+"/category/"+str(category_name)+"/thumbnails/"+img_name
    return thumbnail_path


def use_directory_path(instance, filename):
    return "user_{0}/profile-pics/{1}".format(instance.siteuser.user.id, filename)


def get_user_directory_thumbnail_path(user_id, img_name):
    img_name = img_name.name.split("/")[-1]
    thumbnail_path = settings.MEDIA_ROOT+"/user_{}/banners/thumbnails/{}".format(user_id, img_name)
    return thumbnail_path


def banner_directory_path(instance, filename):
    return "user_{0}/banners/{1}".format(instance.blog_author.user.username.id, filename)


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

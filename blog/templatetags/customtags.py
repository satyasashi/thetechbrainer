from django import template
from siteuser.models import UserFollowing, SiteUser

register = template.Library()


@register.filter(name="getImageName")
def getImageName(path):
    filename = path.split("/")[-1]
    return filename


@register.filter(name="has_group")
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name="follows_author")
def follows_author(user, author):
    siteuser = SiteUser.objects.get(user=user)
    try:
        user_follows_author_check = UserFollowing.objects.get(siteuser=siteuser, following=author)
        if user_follows_author_check:
            return True

    except UserFollowing.DoesNotExist:
        return False

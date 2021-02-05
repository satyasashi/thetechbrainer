from django import template
from user.models import UserFollowing, Profile

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
    try:
        user_follows_author_check = UserFollowing.objects.get(user=user, following=author)
        if user_follows_author_check:
            return True

    except UserFollowing.DoesNotExist:
        return False

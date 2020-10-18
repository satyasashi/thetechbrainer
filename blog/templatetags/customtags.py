from django import template

register = template.Library()


@register.filter(name="getImageName")
def getImageName(path):
    filename = path.split("/")[-1]
    return filename


@register.filter(name="has_group")
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

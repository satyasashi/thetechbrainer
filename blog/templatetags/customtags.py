from django import template

register = template.Library()


@register.filter(name="getImageName")
def getImageName(path):
    filename = path.split("/")[-1]
    return filename

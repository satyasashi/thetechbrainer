from blog.models import BlogPost
from user.models import Notifications
from django.conf import settings


def get_recent_posts_side_box(request):
    blogs = BlogPost.objects.filter(moderator_accepted=True, published=True).order_by("-created_on")[:5]
    # tags = Tag.objects.all()
    # return {"recent_posts": blogs, "tags": tags}
    return {"recent_posts": blogs}


def check_if_moderator_has_notifications(request):
    blogs = BlogPost.objects.filter(submitted_for_moderation=True, published=False)
    if len(blogs) > 0:
        return {"author_waiting_for_publish": True}
    else:
        return {"author_waiting_for_publish": False}


def ga_tracking_id(request):
    return {'ga_tracking_id': settings.GA_TRACKING_ID}


def use_ga(request):
    return {'use_ga': settings.USE_GA}


def new_notifications(request):
    if request.user.is_authenticated:
        notifications = Notifications.objects.filter(notify=request.user)
        unread_notifications = Notifications.objects.filter(notify=request.user, read=False)

        return {"all_notifications": notifications, "unread_notifications": unread_notifications}
    else:
        return {}
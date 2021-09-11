from datetime import datetime
from blog.models import BlogPost


def get_recent_posts_side_box(request):
    blogs = BlogPost.objects.filter(
        moderator_accepted=True, published=True).order_by("-created_on")[:5]
    # tags = Tag.objects.all()
    # return {"recent_posts": blogs, "tags": tags}
    return {"recent_posts": blogs}


def check_if_moderator_has_notifications(request):
    blogs = BlogPost.objects.filter(
        submitted_for_moderation=True, published=False)
    if len(blogs) > 0:
        return {"author_waiting_for_publish": True}
    else:
        return {"author_waiting_for_publish": False}


def current_date(request):
    today_date = datetime.today()
    return {"year": today_date.year}

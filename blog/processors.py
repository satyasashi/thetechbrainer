from blog.models import BlogPost, Tag


def get_recent_posts_side_box(request):
    blogs = BlogPost.objects.all().order_by("-created_on")[:5]
    tags = Tag.objects.all()
    return {"recent_posts": blogs, "tags": tags}


def check_if_moderator_has_notifications(request):
    blogs = BlogPost.objects.filter(submitted_for_moderation=True, published=False)
    print(blogs)
    if len(blogs) > 0:
        return {"author_waiting_for_publish": True}
    else:
        return {"author_waiting_for_publish": False}

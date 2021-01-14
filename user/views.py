from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .models import Profile, UserFollowing
from django.contrib.auth.models import User, Group
from toolbelt.utils import use_directory_path, banner_directory_path
from blog.models import BlogPost, Category
from user.models import UserLikes, UserBookmarks, UserFollowing, PersonalInformation, Notifications
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.text import slugify
from django.db.models import Q

from datetime import datetime

def validate_author_exist_or_not(author_id):
    try:
        author_exists = Profile.objects.filter(id=author_id)
        if len(author_exists) > 0:
            return author_exists[0]
    except Exception as e:
        if e:
            return False


def index(request):
    blogs = BlogPost.objects.filter(
        published=True, moderator_accepted=True,
        preview=False, draft=False
        ).order_by("-created_on")
    query = request.GET.get('q')
    if query:
        blogs = BlogPost.objects.filter(
            published=True, moderator_accepted=True,
            preview=False, draft=False
        )

    paginator = Paginator(blogs, 6)  # 3 blogs per page.
    page = request.GET.get('page')
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)

    return render(request, "index.html", context={'blogs': blogs})


def about(request):
    # authors = User.objects.filter(groups__name="author")
    authors = PersonalInformation.objects.filter(Q(user__groups__name="author") | Q(user__groups__name="moderator"))
    return render(request, "about.html", context={"authors": authors})


def follow(request):
    if request.is_ajax() and request.user.is_authenticated:
        author = validate_author_exist_or_not(request.POST.get('author_id'))
        author = User.objects.get(username=author)
        follows = False
        context = {}

        if author is not False:
            try:
                follow_check = UserFollowing.objects.filter(user=request.user, following=author)
                if len(follow_check) > 0:
                    if follow_check[0].status is True:
                        userfollowObj = follow_check[0]
                        userfollowObj.status = False
                        userfollowObj.save()
                        follows = userfollowObj.status
                        context["follow_obj"] = userfollowObj
                        context["follows"] = follows
                    else:
                        userfollowObj = follow_check[0]
                        userfollowObj.status = True
                        userfollowObj.save()

                        # Add to notification
                        notification = Notifications.objects.create(
                            user=request.user,
                            title="{} has followed you.".format(request.user.username),
                            notify=author
                            )
                        notification.save()

                        follows = userfollowObj.status
                        context["follow_obj"] = userfollowObj
                        context["follows"] = follows

                else:
                    userfollowObj = UserFollowing.objects.create(user=request.user, following=author, status=True)
                    userfollowObj.save()
                    # Add to notification
                    notification = Notifications.objects.create(
                        user=request.user,
                        title="{} has followed you.".format(request.user.username),
                        notify=author
                        )
                    notification.save()
                    
                    follows = userfollowObj.status
                    context["follow_obj"] = userfollowObj
                    context["follows"] = follows

            except Exception:
                pass
            return render(request, "user/ajax/components.html", context)
        else:
            pass
    else:
        return JsonResponse({"error": "Sorry something went wrong. Please try later.", "authenticated": False}, status=300)


@login_required
def user_interests(request):
    if request.method == "POST":
        categories = request.POST.getlist('rGroup')
        all_categories = [cat.category_slug for cat in list(Category.objects.all())]
        check = [True if cat in all_categories else False for cat in categories]

        if True in check:
            userProfile = Profile.objects.get(user=request.user)
            for interest in userProfile.interests.all():
                userProfile.interests.remove(interest)

            for cat in categories:
                userProfile.interests.add(Category.objects.get(category_slug=cat))
                # save_category.save()
            messages.success(request, "Your interests saved.")
            return redirect("user:user_interests")

        elif len(check) == 0:
            messages.error(request, "You should select at least one category.")

            return redirect("user:user_interests")
        else:
            return redirect("user:pagenotfound")
    else:
        categories = Category.objects.all()
        userProfile = Profile.objects.get(user=request.user)
        user_interests = userProfile.interests.all()
        return render(request, "user/interests.html", context={'categories': categories, 'user_interests': user_interests})


def pagenotfound(request):
    return render(request, "pagenotfound.html")


@login_required
def user_drafts(request):
    try:
        author_group = Group.objects.get(name='author')
        moderator_group = Group.objects.get(name='moderator')
    except Group.DoesNotExist:
        return redirect("user:pagenotfound")

    if request.user.groups.filter(name=author_group).exists() or request.user.groups.filter(name=moderator_group).exists():
        blogs = BlogPost.objects.filter(blog_author=request.user, preview=True, draft=True, published=False)
        return render(request, "user/user_drafts.html", context={"blogs": blogs})
    else:
        return redirect("user:pagenotfound")


@login_required
def get_all_tags(request):
    # if request.method == "POST" and request.is_ajax():
    #     tags_list = []
    #     for t in Tag.objects.all():
    #         tags_list.append(t.tag_name)
    #
    #     print(tags_list)
    #     return JsonResponse({"status": "success", "tags": ",".join(tags_list)}, status=200)
    # else:
    #     return JsonResponse({"status": "failure"}, status=404)
    pass


@login_required
def add_new_tag(request):
    pass
#     if request.method == "POST" and request.is_ajax():
#         tag_names = request.POST.get("new_tag")
#         print(tag_names)
#         if len(tag_names) > 0:
#             tag_names = tag_names.split(",")
#             tags_list = {}
#             for tag_name in tag_names:
#                 newtag = Tag.objects.create(
#                     tag_name=tag_name,
#                     tag_slug=slugify(tag_name)
#                 )
#                 newtag.save()
#                 tags_list[newtag.id] = [newtag.id, newtag.tag_name]
#
#             return JsonResponse({"status": "success", "tags": tags_list}, status=200)
#     else:
#         return JsonResponse({"status": "failure"}, status=400)


@login_required
def user_dashboard(request):
    # profile = Profile.objects.get(user=request.user)
    try:
        author_group = Group.objects.get(name='author')

        if request.user.groups.filter(name=author_group).exists():
            user_bookmarks = UserBookmarks.objects.filter(user=request.user)
            following = UserFollowing.objects.filter(user=request.user)
            users_following_you = UserFollowing.objects.filter(following=request.user)
            user_likes = UserLikes.objects.filter(user=request.user, status=True)
            my_blogs_count = BlogPost.objects.filter(blog_author=request.user).count()
            my_blogs_unpublished_count = BlogPost.objects.filter(blog_author=request.user, published=False, draft=True, preview=True).count()
            my_blogs_published_count = BlogPost.objects.filter(blog_author=request.user, published=True, moderator_accepted=True).count()
            my_blogs_moderation_count = BlogPost.objects.filter(blog_author=request.user, moderator_accepted=False, submitted_for_moderation=True).count()

            return render(request, "user/author_dashboard.html", context={
                "user_likes": user_likes,
                "user_bookmarks": user_bookmarks,
                "following": following,
                "users_following_you": users_following_you,
                "my_blogs_count": my_blogs_count,
                "my_blogs_unpublished_count": my_blogs_unpublished_count,
                "my_blogs_published_count": my_blogs_published_count,
                "my_blogs_moderation_count": my_blogs_moderation_count
                })

    except Group.DoesNotExist:
        return redirect("user:pagenotfound")

    try:
        moderator_group = Group.objects.get(name='moderator')
        if request.user.groups.filter(name=moderator_group).exists():
            return redirect("user:moderator_dashboard")
    except Group.DoesNotExist:
        return redirect("user:pagenotfound")

    user_bookmarks = UserBookmarks.objects.filter(user=request.user)
    following = UserFollowing.objects.filter(user=request.user)
    user_likes = UserLikes.objects.filter(user=request.user)

    return render(request, "user/dashboard.html", context={
        "user_likes": user_likes,
        "user_bookmarks": user_bookmarks,
        "following": following
        })


@login_required
def get_user_information(request):
    if request.method == "POST" and request.is_ajax():
        author_id = request.POST.get("id")
        no_social_profile = False
        user = User.objects.get(id=author_id)
        if user.personalinformation.facebook is None and user.personalinformation.github is None and user.personalinformation.twitter is None and user.personalinformation.insta is None and user.personalinformation.linkedin is None:
            no_social_profile = True

        data = JsonResponse({
            "status": "success",
            "no_social_profile": no_social_profile,
            "author_avatar": user.personalinformation.picture.url if user.personalinformation.picture else "/static/img/default_avatar.jpg",
            "author_name": user.username,
            "author_introduction": user.personalinformation.full_introduction,
            "fb": user.personalinformation.facebook,
            "github": user.personalinformation.github,
            "linkedin": user.personalinformation.linkedin,
            "twitter": user.personalinformation.twitter,
            "instagram": user.personalinformation.insta
        }, status=200)

        return data
    else:
        return JsonResponse({"status": "failure", "message": "Author information not found"}, status=400)


@login_required
def unfollow_author(request):
    if request.method == "POST" and request.is_ajax():
        author_id = request.POST.get("author_id")
        # profile = Profile.objects.get(user=request.user)
        try:
            following = User.objects.get(id=author_id)
            user_follows = UserFollowing.objects.get(user=request.user, following=following)
            if user_follows:
                user_follows.delete()
                check_if_no_followers = True if len(UserFollowing.objects.filter(user=request.user)) > 0 else False
                return JsonResponse({"status": "success", "is_still_following": check_if_no_followers,  "title": "Success!", "toast_message": "Successfully Unfollowed Author", "response_type": "success"}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({"title": "Oops!", "toast_message": "Something went wrong. Please try later.", "response_type": "failure"}, status=400)
    else:
        return JsonResponse({"title": "Oops!", "toast_message": "Something went wrong. Please try later.", "response_type": "failure"}, status=400)


@login_required
def moderator_dashboard(request):
    try:
        moderator_group = Group.objects.get(name='moderator')
    except Group.DoesNotExist:
        return redirect("user:pagenotfound")

    try:
        if request.user.groups.filter(name=moderator_group).exists():
            my_blogs_count = BlogPost.objects.filter(blog_author=request.user).count()
            my_blogs_unpublished_count = BlogPost.objects.filter(blog_author=request.user, published=False, draft=True, preview=True).count()
            my_blogs_published_count = BlogPost.objects.filter(blog_author=request.user, published=True, moderator_accepted=True).count()

            author_blogs_moderation_count = BlogPost.objects.filter(moderator_accepted=False, submitted_for_moderation=True).count()

            blogs_for_moderation = BlogPost.objects.filter(submitted_for_moderation=True, moderator_accepted=False, published=False)
            blogs_published = BlogPost.objects.filter(moderator_accepted=True, published=True)

            user_bookmarks = UserBookmarks.objects.filter(user=request.user)
            following = UserFollowing.objects.filter(user=request.user)
            user_likes = UserLikes.objects.filter(user=request.user, status=True)

            return render(request, "user/moderator_dashboard.html", context={
                "blogs_for_moderation": blogs_for_moderation,
                "blogs_published": blogs_published,
                "user_likes": user_likes,
                "user_bookmarks": user_bookmarks,
                "following": following,
                "my_blogs_count": my_blogs_count,
                "my_blogs_unpublished_count": my_blogs_unpublished_count,
                "my_blogs_published_count": my_blogs_published_count,
                "awaiting_moderation_count": author_blogs_moderation_count
                })
    except Profile.DoesNotExist:
        return redirect("user:pagenotfound")


@login_required
def notifications(request):
    unread_notifications = Notifications.objects.filter(read=False, notify=request.user)
    read_notifications = Notifications.objects.filter(read=True, notify=request.user)
    return render(request, "user/notifications.html", context={
        "unread_notifications": unread_notifications,
        "read_notifications": read_notifications
        })


@login_required
def mark_as_read(request):
    if request.is_ajax() and request.method == "POST":
        notification_id = request.POST.get("notification_id")
        try:    
            notification_obj = Notifications.objects.get(id=notification_id)

            # set to read
            notification_obj.read = True
            notification_obj.save()
            return JsonResponse({
                "status": "success", 
                "notification_title": notification_obj.title,
                "url": notification_obj.url,
                "timestamp": datetime.strftime(notification_obj.created_on, "%d %b, %Y")
                }, status=200)

        except Notifications.DoesNotExist as e:
            return JsonResponse({"status": "failure"}, status=400)
    else:
        return JsonResponse({"status": "failure"}, status=400)


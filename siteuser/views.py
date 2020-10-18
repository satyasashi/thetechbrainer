from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .models import SiteUser, UserFollowing
from django.contrib.auth.models import User, Group
from toolbelt.utils import use_directory_path, banner_directory_path
from blog.models import BlogPost, Category
from siteuser.models import UserLikes, UserBookmarks, UserFollowing


def validate_author_exist_or_not(author_id):
    try:
        author_exists = SiteUser.objects.filter(id=author_id)
        if len(author_exists) > 0:
            return author_exists[0]
    except Exception as e:
        if e:
            return False


def index(request):
    blogs = BlogPost.objects.filter(published=True, moderator_accepted=True, preview=False, draft=False)
    return render(request, "index.html", context={'blogs': blogs})


@login_required
def follow(request):
    if request.user.username and request.is_ajax() and request.user.is_authenticated:
        userProfile = SiteUser.objects.get(user=request.user)
        print(request.POST)
        author = validate_author_exist_or_not(request.POST.get('author_id'))
        follows = False
        context = {}
        print("Follow method called.... ", author)

        if author is not False:
            try:
                follow_check = UserFollowing.objects.filter(siteuser=userProfile, following=author)
                print(follow_check)
                if len(follow_check) > 0:
                    if follow_check[0].status is True:
                        userfollowObj = follow_check[0]
                        userfollowObj.status = False
                        userfollowObj.save()
                        follows = userfollowObj.status
                        print(follows)
                        context["follow_obj"] = userfollowObj
                        context["follows"] = follows
                    else:
                        userfollowObj = follow_check[0]
                        userfollowObj.status = True
                        userfollowObj.save()
                        follows = userfollowObj.status
                        context["follow_obj"] = userfollowObj
                        context["follows"] = follows
                        print(follows)

                else:
                    userfollowObj = UserFollowing.objects.create(siteuser=userProfile, following=author, status=True)
                    userfollowObj.save()
                    follows = userfollowObj.status
                    context["follow_obj"] = userfollowObj
                    context["follows"] = follows
                    print(follows)
            except Exception as e:
                if e:
                    print(e)
        return render(request, "user/ajax/components.html", context)
    else:
        print("Not authenticated")
        return JsonResponse({"error": "Sorry something went wrong. Please try later.", "authenticated": False}, status=300)


@login_required
def user_interests(request):
    if request.method == "POST":
        print(request.POST)
        categories = request.POST.getlist('rGroup')
        print("categories passed:", categories)
        all_categories = [cat.category_slug for cat in list(Category.objects.all())]
        print("all categories: ", all_categories)
        check = [True for cat in categories if cat in all_categories]
        print(check)
        if True in check:
            userProfile = SiteUser.objects.get(user=request.user)
            for cat in categories:
                print(cat)
                userProfile.interests.add(Category.objects.get(category_slug=cat))
                # print(save_category)
                # save_category.save()
            messages.success(request, "Your interests saved.")
            return redirect("user:user_interests")
        else:
            return redirect("user:pagenotfound")
    else:
        categories = Category.objects.all()
        # print(categories)
        userProfile = SiteUser.objects.get(user=request.user)
        user_interests = userProfile.interests.all()
        print(user_interests)
        return render(request, "user/interests.html", context={'categories': categories, 'user_interests': user_interests})


def pagenotfound(request):
    return render(request, "pagenotfound.html")


@login_required
def user_drafts(request):
    author_group = Group.objects.get(name='author')
    if request.user.groups.filter(name=author_group).exists():
        blogs = BlogPost.objects.filter(blog_author=SiteUser.objects.get(user=request.user), preview=True, draft=True, published=False)
        return render(request, "user/user_drafts.html", context={"blogs": blogs})
    else:
        return redirect("user:pagenotfound")


@login_required
def user_dashboard(request):
    siteuser = SiteUser.objects.get(user=request.user)
    author_group = Group.objects.get(name='author')
    if request.user.groups.filter(name=author_group).exists():
        pass
    else:
        user_bookmarks = UserBookmarks.objects.filter(user=siteuser)
        following = UserFollowing.objects.filter(siteuser=siteuser)
        user_likes = UserLikes.objects.filter(siteuser=siteuser)
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
        siteuser = SiteUser.objects.get(id=author_id)
        if siteuser.personalinformation.facebook is None and siteuser.personalinformation.github is None and siteuser.personalinformation.twitter is None and siteuser.personalinformation.insta is None:
            no_social_profile = True
            print("Author has no social profile linked")

        data = JsonResponse({
            "status": "success",
            "no_social_profile": no_social_profile,
            "author_avatar": siteuser.personalinformation.picture.url,
            "author_name": siteuser.user.username,
            "author_introduction": siteuser.personalinformation.introduction,
            "fb": siteuser.personalinformation.facebook,
            "github": siteuser.personalinformation.github,
            "linkedin": siteuser.personalinformation.linkedin,
            "twitter": siteuser.personalinformation.twitter,
            "instagram": siteuser.personalinformation.insta
        }, status=200)

        return data
    else:
        return JsonResponse({"status": "failure", "message": "Author information not found"}, status=400)

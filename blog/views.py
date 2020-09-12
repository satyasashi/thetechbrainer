from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import BlogPost, Category, BlogRequest, Tag
from django.http import JsonResponse
from siteuser.models import SiteUser, UserBookmarks, UserFollowing, UserLikes
from django.contrib import messages
from .forms import BlogPostForm

import re
import datetime


# Create your views here.
def blog_search(request):
    if request.method == "POST":
        context = {}
        try:
            # get blog titles with search term.
            search_text = request.POST.get('blogsearch')

            # validation
            pattern = re.compile("[@_!#$%^&*()<>?/\\|}{~:]")

            if pattern.search(search_text) is not None:
                messages.error(request, "No Speacial Characters Are Allowed.")
                return render(request, "blog/search-results.html", context={"messages": messages})
            else:
                blogs = BlogPost.objects.filter(blog_title__icontains=search_text)
                if len(blogs) > 0:
                    context['blogs'] = blogs
                else:
                    context['no_results'] = "no_results"
                return render(request, "blog/search-results.html", context)
        except Exception:
            print(Exception)
            return render(request, "blog/search-results.html", context={"no_results": "no_results"})
    else:
        search = True
        return render(request, "blog/search-results.html", context={"search": search})


def blog_detail(request, slug):
    if slug:
        blog = get_object_or_404(BlogPost, blog_slug=slug)
        if blog:
            context = {'blog': blog}
            authorProfile = blog.blog_author
            if request.user.is_authenticated:
                userProfile = SiteUser.objects.get(user=request.user)
                bookmark = UserBookmarks.objects.filter(user=userProfile, blog_post=blog)
                like = UserLikes.objects.filter(siteuser=userProfile, blog=blog)
                follows_author = UserFollowing.objects.filter(siteuser=userProfile, following=authorProfile)

                if len(follows_author) > 0 and follows_author[0].status is True:
                    context['follows_author'] = 1
                elif len(follows_author) > 0 and follows_author[0].status is False:
                    context['follows_author'] = 0

                if len(bookmark) > 0:
                    context['bookmark'] = 1
                    print("Yes")
                else:
                    context['bookmark'] = 0

                if len(like) > 0:
                    context['like'] = like[0]
                    print("Liked")
                else:
                    context['like'] = False
                    print("Disliked")

                return render(request, "blog/blog_detail.html", context)

            elif request.user.is_anonymous:
                return render(request, "blog/blog_detail.html", context)
        else:
            return render(request, "pagenotfound.html")
    else:
        return render(request, "pagenotfound.html")


def bookmark_blogpost(request, blog_slug):
    if request.user.is_authenticated:
        # Add this blog to bookmark table.
        userProfile = SiteUser.objects.get(user=request.user)
        blog_post = BlogPost.objects.get(blog_slug=blog_slug)
        # check if bookmarked already
        bookmark_status = 0

        try:
            bookmark_check = UserBookmarks.objects.filter(user=userProfile, blog_post=blog_post)
            print(bookmark_check)
            if len(bookmark_check) > 0:
                bookmark_status = 0
                bookmark_check.delete()
            else:
                bookmark = UserBookmarks.objects.create(user=userProfile, blog_post=blog_post)
                bookmark.save()
                bookmark_status = 1
        except Exception as e:
            if e:
                bookmark_status = 0
        return render(request, "blog/ajax/bookmark.html", context={'blog_post': blog_post, 'bookmark_status': bookmark_status})
    else:
        # redirect them to login page, with ?next to current blog they want.
        return JsonResponse({"error": "Sorry something went wrong. Please try later.", "authenticated": False}, status=300)


def like_blogpost(request, blog_slug):
    if request.user.is_authenticated:
        # Add this blog to user likes table.
        userProfile = SiteUser.objects.get(user=request.user)
        blog_post = BlogPost.objects.get(blog_slug=blog_slug)

        try:
            like_check = UserLikes.objects.filter(siteuser=userProfile, blog=blog_post)
            like_status = False
            if len(like_check) > 0:
                print("User likes found")
                # if already liked, then unlike it using FALSE.
                # Else Like it using TRUE
                if like_check[0].status is True:
                    like_check[0].status = False
                    like_check[0].save()
                    like_status = like_check[0].status
                else:
                    like_check[0].status = True
                    like_check[0].save()
                    like_status = like_check[0].status
            else:
                print("User liked this.")

                # Else create new record as User liked it.
                like_obj = UserLikes.objects.create(siteuser=userProfile, blog=blog_post, status=True)
                like_obj.save()
                like_status = like_obj.status

            return JsonResponse({"success": True, "status": like_status}, status=200)
        except Exception as e:
            return JsonResponse({"error": "Sorry something went wrong. Please try later."}, status=300)
    else:
        # redirect them to login page, with ?next to current blog they want.
        return JsonResponse({"error": "Sorry something went wrong. Please try later.", "authenticated": False}, status=300)


def get_categories(request):
    categories = Category.objects.all()
    return render(request, "blog/categories.html", context={"categories": categories})


def filter_by_category(request, category_slug):
    context = {}
    blogs_by_category = BlogPost.objects.filter(blog_category__category_slug = category_slug).order_by("-created_on")
    if len(blogs_by_category) > 0:
        context['category'] = blogs_by_category[0].blog_category
        context['blogs'] = blogs_by_category

        return render(request, "blog/filter_by_category.html", context)
    else:
        category = Category.objects.filter(category_slug=category_slug)
        if len(category) > 0:
            context['category'] = category[0]
            context['no_data'] = True
            return render(request, "blog/filter_by_category.html", context)
        else:
            return redirect("user:pagenotfound")


def filter_by_tag(request, tag_slug):
    context = {}
    blogs_by_tag = BlogPost.objects.filter(blog_tags__tag_slug=tag_slug).order_by("-created_on")
    print(blogs_by_tag)
    if len(blogs_by_tag) > 0:
        context['tag'] = Tag.objects.get(tag_slug=tag_slug)
        context['blogs'] = blogs_by_tag
        return render(request, "blog/filter_by_tag.html", context)
    else:
        return redirect("user:pagenotfound")


def blog_request(request, category_id):
    if request.user.is_authenticated and request.is_ajax():
        # Add a record in 'blog_request' table as user requested.
        # then redirect user to home page with success message.
        try:
            category = Category.objects.get(id=category_id)
            siteuser_obj = SiteUser.objects.get(user=request.user)
            check_blogreq_exists = BlogRequest.objects.filter(siteuser=siteuser_obj, blog_category=category)

            # If record exist, update timestamp. Else create record.
            if len(check_blogreq_exists) > 0:
                # if user already requested, then we save that instance
                # to update the "Timestamp" in BlogRequest table.
                # We shouldn't duplicate the records.
                check_blogreq_exists[0].save()
                return JsonResponse({"success": True, "notified_again": True, "title": "Your request was sent already.", "toast_message": "Stay tuned to receive articles from author.", "response_type": "success"}, status=200)
            else:
                # create a record for user request.
                blogrequest_obj = BlogRequest.objects.create(
                    siteuser=siteuser_obj,
                    blog_category=category
                )
                blogrequest_obj.save()
                return JsonResponse({"success": True, "created": True, "title": "Yay! Your request was successfully sent.", "toast_message": "We've notified the authors.", "response_type": "success"}, status=200)

        except Category.DoesNotExist:
            return JsonResponse({"doesnot_exist": True, "title": "Oops...", "toast_message": "Something went wrong. Please try later.", "response_type": "error"}, status=200)

    else:
        # redirect them to login page, with ?next to current blog they want.
        return JsonResponse({"error": "Sorry something went wrong. Please try later.", "authenticated": False}, status=300)


@login_required
def write_blog(request):
    if request.method == "POST":
        pass
    else:
        new_blog_form = BlogPostForm()
        return render(request, "blog/write_blog.html", context={"new_blog_form": new_blog_form})


@login_required
def preview_blog(request, blog_slug):
    print(request.FILES)
    blog_title = request.POST.get("blog_title")
    blog_subtitle = request.POST.get("blog_subtitle")
    banner_image = request.FILES['banner_image']
    banner_image_source = request.POST.get("banner_image_source")
    content = request.POST.get("content")

    blog_category = request.POST.get("blog_category")
    catgory = Category.objects.get(id=blog_category)

    tags = request.POST.get("blog_tags")
    blog_tags = []
    created_on = datetime.datetime.now().today()

    for tag in tags:
        t = Tag.objects.get(id=tag)
        blog_tags.append(t.tag_name)
    print(blog_tags)

    userProfile = SiteUser.objects.get(user=request.user)

    return render(request, "blog/preview.html", context={"user_profile": userProfile, "blog_title": blog_title, "blog_subtitle": blog_subtitle, "banner_image": banner_image, "banner_image_source": banner_image_source, "content": content, "blog_category": catgory, "blog_tags": blog_tags, "created_on": created_on})

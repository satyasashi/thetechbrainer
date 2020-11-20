from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import BlogPost, Category, BlogRequest
from taggit.models import Tag

from django.http import JsonResponse
from user.models import Profile, UserBookmarks, UserFollowing, UserLikes
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.utils.text import slugify
from .forms import BlogPostForm

import re
import json
import datetime


# views here
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
            return render(request, "blog/search-results.html", context={"no_results": "no_results"})
    else:
        search = True
        return render(request, "blog/search-results.html", context={"search": search})


@login_required
def preview_blog(request, id, blog_slug):
    print(id, blog_slug)
    author_group = Group.objects.get(name='author')
    moderator_group = Group.objects.get(name='moderator')
    print(request.user.groups.filter(name=moderator_group).exists())
    if (request.user.groups.filter(name=author_group).exists()) or (request.user.groups.filter(name=moderator_group).exists()):
        if id and blog_slug:
            print("inside 'if id and blog_slug'")
            try:
                preview_blog = BlogPost.objects.get(id=id, blog_slug=blog_slug, preview=True)
                context = {"blog": preview_blog}

                if preview_blog.submitted_for_moderation is True:
                    context["submitted_for_moderation"] = True
                else:
                    context["submitted_for_moderation"] = False
                    # STOPPED HERE. WRITE BLOG -> PREVIEW -> PREVIEW FROM NEW BLOG
                    # -> EDIT -> EDIT BLOG -> PREVIEW -> PREVIEW BLOG (Check mod submission)

                if request.user.groups.filter(name=moderator_group).exists():
                    context["is_moderator"] = True
                else:
                    context["is_moderator"] = False

                return render(request, "blog/preview_blog.html", context)
            except BlogPost.DoesNotExist as e:
                print(e)
                if e:
                    return render(request, "pagenotfound.html")
        else:
            return redirect("user:pagenotfound")
    else:
        return redirect("user:pagenotfound")


# writing new blog
@login_required
def write_new_blog(request):
    author_group = Group.objects.get(name='author')
    moderator_group = Group.objects.get(name='moderator')
    if request.user.groups.filter(name=author_group).exists() or request.user.groups.filter(name=moderator_group).exists():
        # Check if user is permitted to access this page. Else redirect to 404.
        new_blog_form = BlogPostForm()
        userProfile = Profile.objects.get(user=request.user)

        context = {
            "new_blog_form": new_blog_form,
            "user_profile": userProfile,
        }

        return render(request, "blog/write_blog.html", context)
    else:
        return redirect("user:pagenotfound")


def blog_tags(request):
    tags = [tag.name for tag in Tag.objects.all()]
    print(tags)
    return tags


@login_required
def save_blog_and_show_preview(request):
    author_group = Group.objects.get(name='author')
    moderator_group = Group.objects.get(name='moderator')
    if request.user.groups.filter(name=author_group).exists() or request.user.groups.filter(name=moderator_group).exists():
        if request.method == "POST":
            blogpostform = BlogPostForm(request.POST, request.FILES)

            print(request.POST)
            if blogpostform.is_valid():
                print("Is Valid.")
                print("Cleaned Data: ", blogpostform.cleaned_data)
                blog_post = blogpostform.save(commit=False)
                blog_post.preview = True
                blog_post.draft = True
                blog_post.blog_author = request.user
                blog_post.save()
                # for tags to save use 'save_m2m'
                blogpostform.save_m2m()
                messages.success(request, "Your blog is now saved as draft, check your drafts to publish.")
                return redirect("blog:preview_blog", id=blog_post.id, blog_slug=blog_post.blog_slug)
            else:
                print("errors;")
                messages.errors(request, "Something went wrong. Please make sure all fields are valid.")
                return redirect("blog:write_new_blog")
        else:
            return redirect("blog:write_new_blog")
    else:
        return redirect("user:pagenotfound")


@login_required
def edit_blog(request, id, slug):
    author_group = Group.objects.get(name='author')
    moderator_group = Group.objects.get(name='moderator')
    if request.user.groups.filter(name=author_group).exists() or request.user.groups.filter(name=moderator_group).exists():
        post = get_object_or_404(BlogPost, pk=id)
        if request.method == "POST":
            form = BlogPostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.preview = True
                post.draft = True
                post.save()
                # for tags to save use 'save_m2m'
                form.save_m2m()
                messages.success(request, "Your blog is successfully updated.")
                return redirect("blog:preview_blog", id=post.id, blog_slug=post.blog_slug)
        else:
            edit_form = BlogPostForm(instance=post)
            return render(request, "blog/edit_blog.html", context={"edit_form": edit_form, "post": post})


def bookmark_blogpost(request, id):
    if request.user.is_authenticated:
        # Add this blog to bookmark table.
        blog_post = BlogPost.objects.get(id=id)
        # check if bookmarked already
        bookmark_status = 0

        try:
            bookmark_check = UserBookmarks.objects.filter(user=request.user, blog_post=blog_post)
            if len(bookmark_check) > 0:
                bookmark_status = 0
                bookmark_check.delete()
            else:
                bookmark = UserBookmarks.objects.create(user=request.user, blog_post=blog_post)
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
        blog_post = BlogPost.objects.get(blog_slug=blog_slug)

        try:
            like_check = UserLikes.objects.filter(user=request.user, blog=blog_post)
            like_status = False
            if len(like_check) > 0:
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

                # Else create new record as User liked it.
                like_obj = UserLikes.objects.create(user=request.user, blog=blog_post, status=True)
                like_obj.save()
                like_status = like_obj.status

            return JsonResponse({"success": True, "status": like_status}, status=200)
        except Exception:
            return JsonResponse({"error": "Sorry something went wrong. Please try later."}, status=300)
    else:
        # redirect them to login page, with ?next to current blog they want.
        return JsonResponse({"error": "Sorry something went wrong. Please try later.", "authenticated": False}, status=300)


@login_required
def my_blogs(request):
    # gets all the blogs written by user so far.
    author_group = Group.objects.get(name='author')
    moderator_group = Group.objects.get(name='moderator')

    if request.user.groups.filter(name=author_group).exists() or request.user.groups.filter(name=moderator_group).exists():
        my_blogs = BlogPost.objects.filter(blog_author=request.user)
        return render(request, "blog/my_blogs.html", context={"my_blogs": my_blogs})
    else:
        return redirect("user:pagenotfound")


def blog_request(request, category_id):
    if request.user.is_authenticated and request.is_ajax():
        # Add a record in 'blog_request' table as user requested.
        # then redirect user to home page with success message.
        try:
            category = Category.objects.get(id=category_id)
            check_blogreq_exists = BlogRequest.objects.filter(user=request.user, blog_category=category)

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
                    user=request.user,
                    blog_category=category
                )
                blogrequest_obj.save()
                return JsonResponse({"success": True, "created": True, "title": "Yay! Your request was successfully sent.", "toast_message": "We've notified the authors.", "response_type": "success"}, status=200)

        except Category.DoesNotExist:
            return JsonResponse({"doesnot_exist": True, "title": "Oops...", "toast_message": "Something went wrong. Please try later.", "response_type": "error"}, status=200)

    else:
        # redirect them to login page, with ?next to current blog they want.
        return JsonResponse({"error": "Sorry something went wrong. Please try later.", "authenticated": False}, status=300)


def filter_by_category(request, category_slug):
    context = {}
    blogs_by_category = BlogPost.objects.filter(blog_category__category_slug=category_slug, moderator_accepted=True, published=True).order_by("-created_on")

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


def filter_by_author(request, id):
    blogs_by_author = BlogPost.objects.filter(blog_author__id=id, moderator_accepted=True, published=True).order_by("-created_on")
    if len(blogs_by_author) > 0:
        return render(request, "blog/filter_by_author.html", context={"blogs": blogs_by_author, "author": blogs_by_author[0].blog_author})
    else:
        author = User.objects.get(id=id)
        return render(request, "blog/filter_by_author.html", context={"author": author.username})


def filter_by_tag(request, slug):
    # context = {}
    # blogs_by_tag = BlogPost.objects.filter(blog_tags__slug=tag_slug, moderator_accepted=True, published=True).order_by("-created_on")
    # if len(blogs_by_tag) > 0:
    #     context['tag'] = Tag.objects.get(slug=slug)
    #     context['blogs'] = blogs_by_tag
    #     return render(request, "blog/filter_by_tag.html", context)
    #
    # else:
    #     context['tag'] = Tag.objects.get(slug=slug)
    #     context["no_blogs"] = True
    #     return render(request, "blog/filter_by_tag.html", context)
    pass
    

def get_categories(request):
    categories = Category.objects.all()
    return render(request, "blog/categories.html", context={"categories": categories})


def blog_detail(request, id, slug):
    if slug:
        blog = get_object_or_404(BlogPost, id=id)
        if blog and blog.moderator_accepted and blog.published:
            context = {'blog': blog}
            authorProfile = blog.blog_author
            if request.user.is_authenticated:
                bookmark = UserBookmarks.objects.filter(user=request.user, blog_post=blog)
                like = UserLikes.objects.filter(user=request.user, blog=blog)
                follows_author = UserFollowing.objects.filter(user=request.user, following=authorProfile)

                if len(follows_author) > 0 and follows_author[0].status is True:
                    context['follows_author'] = 1
                elif len(follows_author) > 0 and follows_author[0].status is False:
                    context['follows_author'] = 0

                if len(bookmark) > 0:
                    context['bookmark'] = 1
                else:
                    context['bookmark'] = 0

                if len(like) > 0:
                    context['like'] = like[0]
                else:
                    context['like'] = False

                return render(request, "blog/blog_detail.html", context)

            else:
                return render(request, "blog/blog_detail.html", context)
        else:
            return render(request, "pagenotfound.html")
    else:
        return render(request, "pagenotfound.html")


@login_required
def draft_blog_detail(request, id, slug):
    author_group = Group.objects.get(name='author')
    moderator_group = Group.objects.get(name='moderator')

    if request.user.groups.filter(name=author_group).exists() or request.user.groups.filter(name=moderator_group).exists():
        print("is author")
        if slug:
            blog = get_object_or_404(BlogPost, id=id)
            print("Blog found")
            if blog and blog.moderator_accepted is False and blog.published is False and blog.draft is True:
                context = {'blog': blog}
                # authorProfile = blog.blog_author
                if request.user.is_authenticated:
                    # bookmark = UserBookmarks.objects.filter(user=request.user, blog_post=blog)
                    # like = UserLikes.objects.filter(user=request.user, blog=blog)
                    # follows_author = UserFollowing.objects.filter(user=request.user, following=authorProfile)
                    if request.user.groups.filter(name=moderator_group).exists():
                        context["is_moderator"] = True
                    return render(request, "blog/preview_blog.html", context)

                else:
                    return render(request, "blog/blog_detail.html", context)
            else:
                return redirect("user:pagenotfound")
    else:
        return redirect("user:pagenotfound")


@login_required
def submit_for_moderation(request):
    author_group = Group.objects.get(name='author')
    if request.user.groups.filter(name=author_group).exists():
        if request.is_ajax() and request.method == "POST":
            if request.POST.get("type") == "submitForModerationPreview":
                blog_id = request.POST.get("blog_id")
                blog = get_object_or_404(BlogPost, id=blog_id)
                blog.preview = True
                blog.draft = False
                blog.submitted_for_moderation = True
                blog.save()
                messages.success(request, "Your blog has been submitted for moderation.")
                return JsonResponse({"status": "success", "redirect_to": "/"}, status=200)
            else:
                return redirect("user:pagenotfound")
    else:
        return redirect("user:pagenotfound")


@login_required
def awaiting_moderation_blog_detail(request, id, slug):
    author_group = Group.objects.get(name='author')
    if request.user.groups.filter(name=author_group).exists():
        if slug:
            blog = get_object_or_404(BlogPost, id=id)
            if blog and blog.moderator_accepted is False and blog.published is False and blog.submitted_for_moderation is True:
                context = {'blog': blog, 'submitted_for_moderation': True}
                authorProfile = blog.blog_author
                if request.user.is_authenticated:
                    bookmark = UserBookmarks.objects.filter(user=request.user, blog_post=blog)
                    like = UserLikes.objects.filter(user=request.user, blog=blog)
                    follows_author = UserFollowing.objects.filter(user=request.user, following=authorProfile)

                    return render(request, "blog/preview_blog.html", context)

                else:
                    return render(request, "blog/blog_detail.html", context)
            else:
                return redirect("user:pagenotfound")
    else:
        return redirect("user:pagenotfound")


@login_required
def accept_and_publish(request, id):
    moderator_group = Group.objects.get(name='moderator')
    # check if author of blog is moderator.
    check_author_of_blog = BlogPost.objects.get(id=id)
    if check_author_of_blog.blog_author.groups.filter(name=moderator_group).exists():
        check_author_of_blog.preview = False
        check_author_of_blog.draft = False
        check_author_of_blog.moderator_accepted = True
        check_author_of_blog.submitted_for_moderation = True
        check_author_of_blog.published = True
        check_author_of_blog.save()

        messages.success(request, "Blog has been successfully published.")
        return JsonResponse({"status": "success", "redirect_to": "/"}, status=200)

    if request.method == "POST" and request.is_ajax() and request.user.groups.filter(name=moderator_group).exists():
        # blog_id = request.POST.get("blog_id")
        try:
            blog_post = BlogPost.objects.get(id=id, submitted_for_moderation=True, moderator_accepted=False)
            if blog_post:
                blog_post.preview = False
                blog_post.draft = False
                blog_post.moderator_accepted = True
                blog_post.submitted_for_moderation = True
                blog_post.published = True
                blog_post.save()

                messages.success(request, "Blog has been successfully published.")
                return JsonResponse({"status": "success", "redirect_to": "/"}, status=200)
        except BlogPost.DoesNotExist:
            return JsonResponse({"status": "failure"}, status=400)
    else:
        # messages.success(request, "Blog has been successfully published.")
        return JsonResponse({"status": "failure"}, status=400)

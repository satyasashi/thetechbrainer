from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import BlogPost, Category, BlogRequest
from django.http import JsonResponse
from siteuser.models import SiteUser, UserBookmarks, UserFollowing, UserLikes
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.utils.text import slugify
from .forms import BlogPostForm, BlogPostEditForm

import re
import json
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
            return render(request, "blog/search-results.html", context={"no_results": "no_results"})
    else:
        search = True
        return render(request, "blog/search-results.html", context={"search": search})


def blog_detail(request, slug):
    if slug:
        blog = get_object_or_404(BlogPost, blog_slug=slug)
        if blog and blog.moderator_accepted and blog.published:
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


def bookmark_blogpost(request, blog_slug):
    if request.user.is_authenticated:
        # Add this blog to bookmark table.
        userProfile = SiteUser.objects.get(user=request.user)
        blog_post = BlogPost.objects.get(blog_slug=blog_slug)
        # check if bookmarked already
        bookmark_status = 0

        try:
            bookmark_check = UserBookmarks.objects.filter(user=userProfile, blog_post=blog_post)
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
                like_obj = UserLikes.objects.create(siteuser=userProfile, blog=blog_post, status=True)
                like_obj.save()
                like_status = like_obj.status

            return JsonResponse({"success": True, "status": like_status}, status=200)
        except Exception:
            return JsonResponse({"error": "Sorry something went wrong. Please try later."}, status=300)
    else:
        # redirect them to login page, with ?next to current blog they want.
        return JsonResponse({"error": "Sorry something went wrong. Please try later.", "authenticated": False}, status=300)


def get_categories(request):
    categories = Category.objects.all()
    return render(request, "blog/categories.html", context={"categories": categories})


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


def filter_by_tag(request, tag_slug):
    # context = {}
    # blogs_by_tag = BlogPost.objects.filter(blog_tags__tag_slug=tag_slug, moderator_accepted=True, published=True).order_by("-created_on")
    # if len(blogs_by_tag) > 0:
    #     context['tag'] = Tag.objects.get(tag_slug=tag_slug)
    #     context['blogs'] = blogs_by_tag
    #     return render(request, "blog/filter_by_tag.html", context)
    #
    # else:
    #     context['tag'] = Tag.objects.get(tag_slug=tag_slug)
    #     context["no_blogs"] = True
    #     return render(request, "blog/filter_by_tag.html", context)
    pass


def filter_by_author(request, id):
    blogs_by_author = BlogPost.objects.filter(blog_author__id=id, moderator_accepted=True, published=True).order_by("-created_on")
    if len(blogs_by_author) > 0:
        return render(request, "blog/filter_by_author.html", context={"blogs": blogs_by_author, "author": blogs_by_author[0].blog_author})
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
def preview_blog(request, id, blog_slug):
    author_group = Group.objects.get(name='author')
    moderator_group = Group.objects.get(name='moderator')
    if (request.user.groups.filter(name=author_group).exists()) or (request.user.groups.filter(name=moderator_group).exists()):
        if id and blog_slug:
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
                    context["moderator"] = True
                else:
                    context["moderator"] = False

                return render(request, "blog/preview_blog.html", context)
            except BlogPost.DoesNotExist as e:
                if e:
                    return render(request, "pagenotfound.html")
        else:
            return redirect("user:pagenotfound")
    else:
        return redirect("user:pagenotfound")


@login_required
def submitted_mod_preview(request, id, blog_slug):
    author_group = Group.objects.get(name='author')
    moderator_group = Group.objects.get(name='moderator')
    if (request.user.groups.filter(name=author_group).exists()) or (request.user.groups.filter(name=moderator_group).exists()):
        if id and blog_slug:
            try:
                preview_blog = BlogPost.objects.get(id=id, blog_slug=blog_slug, preview=True)
                context = {"blog": preview_blog}
                return render(request, "blog/submitted_mod_preview.html", context)
            except BlogPost.DoesNotExist as e:
                if e:
                    return render(request, "pagenotfound.html")
        else:
            return redirect("user:pagenotfound")
    else:
        return redirect("user:pagenotfound")


@login_required
def edit_blog(request, id, blog_slug):
    print("Edit blog")
    author_group = Group.objects.get(name='author')
    moderator_group = Group.objects.get(name='moderator')

    if request.user.groups.filter(name=author_group).exists():
        if request.method == "POST" and request.POST.get("type") != "":
            if id and blog_slug:
                author = SiteUser.objects.get(user=request.user)
                edit_blog = BlogPost.objects.get(id=id, blog_slug=blog_slug)
                form = BlogPostEditForm(request.POST, request.FILES, instance=edit_blog)
                # print(request.POST.getlist("blog_tags"))
                if form.is_valid():
                    edit_blog_post = form.save(commit=False)
                    if request.POST.get("type") == "preview":
                        print("edit_blog type is preview")
                        edit_blog_post.preview = True
                        edit_blog_post.submitted_for_moderation = False
                        edit_blog_post.draft = True

                    elif request.POST.get("type") == "submitForModeration":
                        edit_blog_post.submitted_for_moderation = True

                    edit_blog_post.blog_author = author
                    edit_blog_post.save()

                    return redirect("blog:preview_blog", id=edit_blog_post.id, blog_slug=edit_blog_post.blog_slug)
                else:
                    return redirect("blog:edit_blog_post", id=id, blog_slug=blog_slug)
            else:
                return render(request, "pagenotfound.html")
        else:
            context = {}
            if id and blog_slug:
                author = SiteUser.objects.get(user=request.user)
                edit_blog = BlogPost.objects.get(id=id, blog_slug=blog_slug)
                print("Edit blog else", request.user.groups.all())

                if edit_blog.submitted_for_moderation is True:
                    print("Blog Submitted For Moderation")
                    context["submitted_for_moderation"] = True

                if request.user.groups.filter(name=moderator_group).exists():
                    print("moderator yes")
                    context["is_moderator"] = True

                form = BlogPostEditForm(instance=edit_blog)
                # context = {"edit_blog_form": form, "edit_blog_post": edit_blog, "tags": tags}
                context["edit_blog_form"] = form
                context["edit_blog_post"] = edit_blog
                return render(request, "blog/edit_blog.html", context)
    else:
        return redirect("user:pagenotfound")


@login_required
def submitted_blog_edit(request, id, blog_slug):
    author_group = Group.objects.get(name='author')
    if request.user.groups.filter(name=author_group).exists():
        if request.method == "POST" and request.POST.get("type") != "":
            if id and blog_slug:
                author = SiteUser.objects.get(user=request.user)
                edit_blog = BlogPost.objects.get(id=id, blog_slug=blog_slug)
                form = BlogPostEditForm(request.POST, request.FILES, instance=edit_blog)
                # print(request.POST.getlist("blog_tags"))
                if form.is_valid():
                    edit_blog_post = form.save(commit=False)
                    if request.POST.get("type") == "submittedModPreview":
                        print("submittedModPreview")
                        edit_blog_post.preview = True

                    edit_blog_post.blog_author = author
                    edit_blog_post.save()

                    return redirect("blog:submitted_mod_preview", id=edit_blog_post.id, blog_slug=edit_blog_post.blog_slug)
                else:
                    return redirect("blog:edit_blog_post", id=id, blog_slug=blog_slug)
            else:
                return render(request, "pagenotfound.html")
        else:
            if id and blog_slug:
                author = SiteUser.objects.get(user=request.user)
                edit_blog = BlogPost.objects.get(id=id, blog_slug=blog_slug)
                # tags = Tag.objects.all()

                form = BlogPostEditForm(instance=edit_blog)
                # context = {"edit_blog_form": form, "edit_blog_post": edit_blog, "tags": tags}
                context = {"edit_blog_form": form, "edit_blog_post": edit_blog}
                return render(request, "blog/edit_blog.html", context)
    else:
        return redirect("user:pagenotfound")


# new view
@login_required
def preview_from_new_blog(request):
    # author writes new blog & clicks preview first time.
    author_group = Group.objects.get(name='author')
    moderator_group = Group.objects.get(name='moderator')
    if request.user.groups.filter(name=author_group).exists() or request.user.groups.filter(name=moderator_group).exists():
        if request.method == "POST" and request.POST.get("type") == "preview":
            new_blog_form = BlogPostForm(request.POST, request.FILES)
            author = SiteUser.objects.get(user=request.user)

            if new_blog_form.is_valid():
                new_blog_obj = new_blog_form.save(commit=False)
                new_blog_obj.preview = True
                new_blog_obj.draft = True
                new_blog_obj.blog_author = author
                new_blog_obj.save()

                messages.info(request, "Your blog is saved in your drafts. Please check it there.")
                return redirect("blog:preview_blog", id=new_blog_obj.id, blog_slug=new_blog_obj.blog_slug)
            else:
                print(new_blog_form.errors)
                messages.error(request, "Something went wrong. Please check if all fields are filled.")
                return redirect("blog:write_blog")
    else:
        return redirect("user:pagenotfound")


# new view
@login_required
# def preview_from_edit_blog(request):
#     # author edits blog & clicks preview.
#     author_group = Group.objects.get(name='author')
#     moderator_group = Group.objects.get(name='moderator')
#     if request.user.groups.filter(name=author_group).exists() or request.user.groups.filter(name=moderator_group).exists():
#         if request.method == "POST" and request.POST.get("type") == "preview":
#             edit_blog_form = BlogPostEditForm(request.POST, request.FILES)
#             author = SiteUser.objects.get(user=request.user)
#
#             if edit_blog_form.is_valid():
#                 edit_blog_obj = edit_blog_form.save(commit=False)
#                 edit_blog_obj.preview = True
#                 edit_blog_obj.draft = False
#                 edit_blog_obj.blog_author = author
#                 edit_blog_obj.save()
#
#                 messages.info(request, "Your blog has been updated.")
#                 return redirect("blog:preview_blog", id=edit_blog_obj.id, blog_slug=edit_blog_obj.blog_slug)
#             else:
#                 print(edit_blog_form.errors)
#                 messages.error(request, "Something went wrong. Please check if all fields are filled.")
#                 return redirect("user:user_drafts")
#     else:
#         return redirect("user:pagenotfound")


# new view
@login_required
# def submit_blog_for_moderation(request):
#     # when Author finishes writing blog and hits
#     # "Submit for moderation" button on preview page.
#     author_group = Group.objects.get(name='author')
#     moderator_group = Group.objects.get(name='moderator')
#     if request.user.groups.filter(name=author_group).exists() or request.user.groups.filter(name=moderator_group).exists():
#         if request.method == "POST" and request.POST.get("type") == "submitForModeration":
#             blog_form = BlogPostEditForm(request.POST, request.FILES)
#             author = SiteUser.objects.get(user=request.user)
#             if blog_form.is_valid():
#                 blog_obj = blog_form.save(commit=False)
#                 blog_obj.preview = False
#                 if blog_form.cleaned_data["banner_image"] is None:
#                     pass
#                 blog_obj.draft = False
#                 blog_obj.submitted_for_moderation = True
#                 blog_obj.blog_author = author
#                 blog_obj.save()
#
#                 messages.success(request, "Your blog is submitted for moderation. You'll hear from moderator soon!")
#                 return redirect("user:index")
#             else:
#                 pass
#     else:
#         return redirect("user:pagenotfound")


@login_required
def write_blog(request):
    author_group = Group.objects.get(name='author')
    moderator_group = Group.objects.get(name='moderator')
    if request.user.groups.filter(name=author_group).exists() or request.user.groups.filter(name=moderator_group).exists():
        new_blog_form = BlogPostForm()
        userProfile = SiteUser.objects.get(user=request.user)

        context = {
            "new_blog_form": new_blog_form,
            "user_profile": userProfile,
        }
        return render(request, "blog/write_blog.html", context)
    else:
        return redirect("user:pagenotfound")


@login_required
# def write_blog_from_edit_page(request):
#     author_group = Group.objects.get(name='author')
#     moderator_group = Group.objects.get(name='moderator')
#     if request.user.groups.filter(name=author_group).exists() or request.user.groups.filter(name=moderator_group).exists():
#         if request.method == "POST" and request.POST.get("type") == "preview":
#             new_blog_form = BlogPostEditForm(request.POST, request.FILES)
#             author = SiteUser.objects.get(user=request.user)
#
#             if new_blog_form.is_valid():
#                 new_blog_obj = new_blog_form.save(commit=False)
#                 new_blog_obj.preview = True
#                 new_blog_obj.draft = True
#                 new_blog_obj.blog_author = author
#                 new_blog_obj.save()
#                 # for tag in new_blog_form.cleaned_data["blog_tags"]:
#                 #     new_blog_obj.blog_tags.add(tag)
#                 #     new_blog_obj.save()
#
#                 messages.info(request, "Your blog is saved in your drafts. Please check it there.")
#                 return redirect("blog:preview_blog", id=new_blog_obj.id, blog_slug=new_blog_obj.blog_slug)
#             else:
#                 print(new_blog_form.errors)
#                 messages.error(request, "Something went wrong. Please check if all fields are filled.")
#                 return redirect("blog:write_blog")
#
#         elif request.method == "POST" and request.POST.get("type") == "submitForModeration":
#             blog_form = BlogPostEditForm(request.POST, request.FILES)
#             author = SiteUser.objects.get(user=request.user)
#             if blog_form.is_valid():
#                 blog_obj = blog_form.save(commit=False)
#                 blog_obj.preview = False
#                 if blog_form.cleaned_data["banner_image"] is None:
#                     pass
#                 blog_obj.draft = False
#                 blog_obj.submitted_for_moderation = True
#                 blog_obj.blog_author = author
#                 blog_obj.save()
#
#                 # for tag in blog_form.cleaned_data["blog_tags"]:
#                 #     new_blog_obj.blog_tags.add(tag)
#                 #     new_blog_obj.save()
#
#                 messages.success(request, "Your blog is submitted for moderation. You'll hear from moderator soon!")
#                 return redirect("user:index")
#             else:
#                 pass
#         else:
#             new_blog_form = BlogPostForm()
#             userProfile = SiteUser.objects.get(user=request.user)
#             # tags_list = []
#             # for t in Tag.objects.all():
#             #     tags_list.append(t.tag_name)
#
#             context = {
#                 "new_blog_form": new_blog_form,
#                 "user_profile": userProfile,
#                 # "tags": ",".join(tags_list)
#             }
#             return render(request, "blog/write_blog.html", context)
#     else:
#         return redirect("user:pagenotfound")


@login_required
# def submit_for_moderation_preview(request):
#     author_group = Group.objects.get(name='author')
#     if request.user.groups.filter(name=author_group).exists():
#         if request.is_ajax() and request.method == "POST":
#             if request.POST.get("type") == "submitForModerationPreview":
#                 blog_id = request.POST.get("blog_id")
#                 blog = get_object_or_404(BlogPost, id=blog_id)
#                 blog.preview = False
#                 blog.draft = False
#                 blog.submitted_for_moderation = True
#                 blog.save()
#                 messages.success(request, "Your blog has been submitted for moderation.")
#                 return JsonResponse({"status": "success", "redirect_to": "/"}, status=200)
#             else:
#                 return redirect("user:pagenotfound")
#     else:
#         return redirect("user:pagenotfound")


@login_required
def draft_blog_detail(request, slug):
    author_group = Group.objects.get(name='author')
    if request.user.groups.filter(name=author_group).exists():
        if slug:
            blog = get_object_or_404(BlogPost, blog_slug=slug)
            if blog and blog.moderator_accepted is False and blog.published is False and blog.draft is True:
                context = {'blog': blog}
                authorProfile = blog.blog_author
                if request.user.is_authenticated:
                    userProfile = SiteUser.objects.get(user=request.user)
                    bookmark = UserBookmarks.objects.filter(user=userProfile, blog_post=blog)
                    like = UserLikes.objects.filter(siteuser=userProfile, blog=blog)
                    follows_author = UserFollowing.objects.filter(siteuser=userProfile, following=authorProfile)

                    return render(request, "blog/preview_blog.html", context)

                else:
                    return render(request, "blog/blog_detail.html", context)
            else:
                return redirect("user:pagenotfound")
    else:
        return redirect("user:pagenotfound")


@login_required
def awaiting_moderation_blog_detail(request, slug):
    author_group = Group.objects.get(name='author')
    if request.user.groups.filter(name=author_group).exists():
        if slug:
            blog = get_object_or_404(BlogPost, blog_slug=slug)
            if blog and blog.moderator_accepted is False and blog.published is False and blog.submitted_for_moderation is True:
                context = {'blog': blog, 'submitted_for_moderation': True}
                authorProfile = blog.blog_author
                if request.user.is_authenticated:
                    userProfile = SiteUser.objects.get(user=request.user)
                    bookmark = UserBookmarks.objects.filter(user=userProfile, blog_post=blog)
                    like = UserLikes.objects.filter(siteuser=userProfile, blog=blog)
                    follows_author = UserFollowing.objects.filter(siteuser=userProfile, following=authorProfile)

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
    if check_author_of_blog.blog_author.user.groups.filter(name=moderator_group).exists():
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


@login_required
def my_blogs(request):
    # gets all the blogs written by user so far.
    author_group = Group.objects.get(name='author')
    moderator_group = Group.objects.get(name='moderator')

    if request.user.groups.filter(name=author_group).exists() or request.user.groups.filter(name=moderator_group).exists():
        siteuser = SiteUser.objects.get(user=request.user)
        my_blogs = BlogPost.objects.filter(blog_author=siteuser)
        return render(request, "blog/my_blogs.html", context={"my_blogs": my_blogs})
    else:
        return redirect("user:pagenotfound")

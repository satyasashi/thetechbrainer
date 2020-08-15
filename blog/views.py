from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BlogPost, Category
from django.http import JsonResponse
from siteuser.models import SiteUser, UserBookmarks, UserFollowing
from django.contrib import messages

import re


# Create your views here.
def blog_search(request):
    if request.method == "POST":
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
                print(blogs)
                return render(request, "blog/search-results.html", context={"blogs": blogs})
        except Exception:
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

                return render(request, "blog/blog_detail.html", context)

            elif request.user.is_anonymous:
                return render(request, "blog/blog_detail.html", context)
        else:
            return render(request, "pagenotfound.html")
    else:
        return render(request, "pagenotfound.html")


@login_required
def bookmark_blogpost(request, blog_slug):
    print("Blog slug: ", blog_slug)
    if request.user.username:
        print("no username")
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
                print(e)
                bookmark_status = 0
        return render(request, "blog/ajax/bookmark.html", context={'blog_post': blog_post, 'bookmark_status': bookmark_status})
    else:
        print("Not authenticated")
        return JsonResponse({"error": "Sorry something went wrong. Please try later.", "authenticated": False}, status=300)

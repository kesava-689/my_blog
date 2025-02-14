from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
# from datetime import date
from .models import Post
from django.views.generic import ListView, DetailView
from django.views import View
from .form import CommentForm
# Create your views here.
POSTS = [
    # {
    #     "slug" : "hike-in-the-mountains",
    #     "image" : "Mountain.jpg",
    #     "author" : "ChennaKesava",
    #     "date" : date(2024, 8, 17),
    #     "title" : "Mountain Hiking",
    #     "excerpt" : "Lorem ipsum dolor sit amet consectetur adipisicing elit. Suscipit cumque delectus sunt dolorum. Distinctio iusto, quod atque, impedit aut optio, ad quaerat hic quisquam quam laudantium natus consequatur dolorem obcaecati!",
    #     "content" : """
    #             Lorem ipsum dolor sit amet consectetur adipisicing elit. Suscipit cumque delectus sunt dolorum. Distinctio iusto, quod atque, impedit aut optio, ad quaerat hic quisquam quam laudantium natus consequatur dolorem obcaecati!
                
    #             Lorem ipsum dolor sit amet consectetur adipisicing elit. Suscipit cumque delectus sunt dolorum. Distinctio iusto, quod atque, impedit aut optio, ad quaerat hic quisquam quam laudantium natus consequatur dolorem obcaecati!
                
    #             Lorem ipsum dolor sit amet consectetur adipisicing elit. Suscipit cumque delectus sunt dolorum. Distinctio iusto, quod atque, impedit aut optio, ad quaerat hic quisquam quam laudantium natus consequatur dolorem obcaecati!
    #         """
    # },
    # {
    #     "slug" : "programming-is-fun",
    #     "image" : "Coding.jpg",
    #     "author" : "ChennaKesava",
    #     "date" : date(2022, 8, 17),
    #     "title" : "Programming is great!",
    #     "excerpt" : "Lorem ipsum dolor sit amet consectetur adipisicing elit. Suscipit cumque delectus sunt dolorum. Distinctio iusto, quod atque, impedit aut optio, ad quaerat hic quisquam quam laudantium natus consequatur dolorem obcaecati!",
    #     "content" : """
    #             Lorem ipsum dolor sit amet consectetur adipisicing elit. Suscipit cumque delectus sunt dolorum. Distinctio iusto, quod atque, impedit aut optio, ad quaerat hic quisquam quam laudantium natus consequatur dolorem obcaecati!
                
    #             Lorem ipsum dolor sit amet consectetur adipisicing elit. Suscipit cumque delectus sunt dolorum. Distinctio iusto, quod atque, impedit aut optio, ad quaerat hic quisquam quam laudantium natus consequatur dolorem obcaecati!
                
    #             Lorem ipsum dolor sit amet consectetur adipisicing elit. Suscipit cumque delectus sunt dolorum. Distinctio iusto, quod atque, impedit aut optio, ad quaerat hic quisquam quam laudantium natus consequatur dolorem obcaecati!
    #             """
    # },
    # {
    #     "slug" : "into-the-woods",
    #     "image" : "Wood.jpg",
    #     "author" : "ChennaKesava",
    #     "date" : date(2022,6, 17),
    #     "title" : "Nature At Its Best!",
    #     "excerpt" : "Lorem ipsum dolor sit amet consectetur adipisicing elit. Suscipit cumque delectus sunt dolorum. Distinctio iusto, quod atque, impedit aut optio, ad quaerat hic quisquam quam laudantium natus consequatur dolorem obcaecati!",
    #     "content" : """
    #             Lorem ipsum dolor sit amet consectetur adipisicing elit. Suscipit cumque delectus sunt dolorum. Distinctio iusto, quod atque, impedit aut optio, ad quaerat hic quisquam quam laudantium natus consequatur dolorem obcaecati!
                
    #             Lorem ipsum dolor sit amet consectetur adipisicing elit. Suscipit cumque delectus sunt dolorum. Distinctio iusto, quod atque, impedit aut optio, ad quaerat hic quisquam quam laudantium natus consequatur dolorem obcaecati!
                
    #             Lorem ipsum dolor sit amet consectetur adipisicing elit. Suscipit cumque delectus sunt dolorum. Distinctio iusto, quod atque, impedit aut optio, ad quaerat hic quisquam quam laudantium natus consequatur dolorem obcaecati!
    #             """
    # },
]

# def get_date(POSTS):
#     return POSTS['date']



class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"
    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data
# def starting_page(request):
#     latest_posts = Post.objects.all().order_by("-date")[:3]
#     return render(request, "blog/index.html",{
#         "posts":latest_posts
#     })



class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"
# def posts(request):
#     all_posts = Post.objects.all().order_by("-date")
#     return render(request, "blog/all-posts.html",{
#         "all_posts" : all_posts
#     })




class DetailPostView(View):
    def is_stored_posts(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False
        return is_saved_for_later
    
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        
        context = {
            "post":post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later":self.is_stored_posts(request, post.id)
        }
        return render(request, "blog/post-detail.html",context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post_detail_page", args=[slug]))
        
        context = {
            "post":post,
            "post_tags": post.tags.all(),
            "comment_form": comment_form,
            "comments":post.comments.all().order_by("-id"),
            "saved_for_later":self.is_stored_posts(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)
        
        
# def post_detai    ls(request, slug):
#     # identified_post = next(post for post in POSTS if post['slug']==slug)
#     identified_post = get_object_or_404(Post, slug = slug)
#     return render(request, "blog/post-detail.html",{
#         "post":identified_post,
#         "post_tags":identified_post.tags.all()
#     })
class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")

        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True
        return render(request, "blog/stored-posts.html", context)

    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)
        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect("/")
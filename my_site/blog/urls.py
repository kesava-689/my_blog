from django.urls import path
from . import views




urlpatterns = [
    path("", views.StartingPageView.as_view(), name="starting_page"),
    path("posts", views.AllPostsView.as_view(), name="posts_page"),
    path("posts/<slug:slug>", views.DetailPostView.as_view(), name="post_detail_page"),
    path("read-later", views.ReadLaterView.as_view(), name="read_later")
]

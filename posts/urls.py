from django.urls import path

from . import views


urlpatterns = [
    path("list/", views.PostListAPIView.as_view(), name="list"),
    path("create/", views.PostCreateAPIView.as_view(), name="create"),
    path("detail/<int:id>", views.PostDetailAPIView.as_view(), name="detail"),
    path("like/<int:id>", views.PostLikeAPIView.as_view(), name="like"),
    path("dislike/<int:id>", views.PostDislikeAPIView.as_view(), name="dislike"),
    path(
        "likes-list/<int:post_id>", views.LikeListAPIView.as_view(), name="likes-list"
    ),
    path(
        "dislikes-list/<int:post_id>",
        views.DislikeListAPIView.as_view(),
        name="dislikes-list",
    ),
]

from django.urls import path

from . import views


urlpatterns = [
    path("list/", views.PostListAPIView.as_view(), name="list"),
    path("create/", views.PostCreateAPIView.as_view(), name="create"),
    path("detail/<int:id>", views.PostDetailAPIView.as_view(), name="detail"),
    path("like/<int:id>", views.PostLikeAPIView.as_view(), name="like"),
    path(
        "analytics/likes/", views.LikeAnalyticsAPIView.as_view(), name="likes-analytics"
    ),
    path(
        "likes-list/<int:post_id>", views.LikeListAPIView.as_view(), name="likes-list"
    ),
]

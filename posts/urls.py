from django.urls import path

from . import views


urlpatterns = [
    path("list/", views.PostListAPIView.as_view(), name="list"),
    path("create/", views.PostCreateAPIView.as_view(), name="create"),
    path("detail/<int:id>", views.PostDetailAPIView.as_view(), name="detail"),
]

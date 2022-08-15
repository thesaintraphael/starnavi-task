from django.db.models import Count
from django.db.models.functions import ExtractDay

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework.backends import DjangoFilterBackend

from .filters import LikeFilter
from .utils import PostActionUtil
from .models import Like, Post
from .serializers import AnalyticsSerializer, LikeSerializer, PostSerializer
from mainapp.api.permissions import IsAuthorOrReadOnly


class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        IsAuthenticated,
        IsAuthorOrReadOnly,
    )
    lookup_field = "id"


class PostLikeAPIView(generics.GenericAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "id"

    def get(self, request, *args, **kwargs):

        post = self.get_object()
        PostActionUtil(post).create_or_delete_like(request.user)

        serializer = self.serializer_class(instance=post)

        return Response(serializer.data, status=200)


class LikeListAPIView(generics.ListAPIView):

    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def get(self, request, post_id, *args, **kwargs):

        serializer = self.serializer_class(
            self.queryset.filter(post__id=post_id), many=True
        )

        return Response(serializer.data)


class LikeAnalyticsAPIView(generics.ListAPIView):

    queryset = Like.objects.all()
    serializer_class = AnalyticsSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = LikeFilter
    pagination_class = None

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(day=ExtractDay("created_at"))
            .values("day")
            .annotate(likes_count=Count("id"))
            .order_by("day")
        )

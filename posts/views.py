from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Post
from .serializers import PostSerializer
from .utils import PostActionUtil
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


class PostDislikeAPIView(PostLikeAPIView):
    def get(self, request, *args, **kwargs):

        post = self.get_object()
        PostActionUtil(post).create_or_delete_dislike(request.user)

        serializer = self.serializer_class(instance=post)

        return Response(serializer.data, status=200)

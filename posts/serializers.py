from rest_framework import serializers

from .models import Dislike, Like, Post


class PostSerializer(serializers.ModelSerializer):

    likes_count = serializers.IntegerField(source="get_likes_count", read_only=True)
    dislikes_count = serializers.IntegerField(
        source="get_dislikes_count", read_only=True
    )

    class Meta:
        model = Post
        fields = "__all__"
        extra_kwargs = {"author": {"read_only": True}}


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        exclude = ("-updated_at",)
        extra_kwargs = {"author": {"read_only": True}}


class DislikeSerializer(LikeSerializer):
    class Meta(LikeSerializer.Meta):
        model = Dislike

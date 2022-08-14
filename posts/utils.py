from django.contrib.auth import get_user_model

from .models import Post, Like, Dislike


User = get_user_model()


class PostActionUtil:
    def __init__(self, post: Post) -> None:
        self.post = post

    def create_or_delete_like(self, user: User) -> None:

        if self.post.likes.filter(author=user).exists():
            self.post.likes.filter(author=user).delete()

        else:
            Like.objects.create(author=user, post=self.post)
            self.post.dislikes.filter(author=user).delete()

    def create_or_delete_dislike(self, user: User) -> None:

        if self.post.dislikes.filter(author=user).exists():
            self.post.dislikes.filter(author=user).delete()

        else:
            Dislike.objects.create(author=user, post=self.post)
            self.post.likes.filter(author=user).delete()

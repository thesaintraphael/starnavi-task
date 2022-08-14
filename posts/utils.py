from django.contrib.auth import get_user_model

from .models import Post, Like


User = get_user_model()


class PostActionUtil:
    def __init__(self, post: Post) -> None:
        self.post = post

    def create_or_delete_like(self, user: User) -> None:

        if self.post.likes.filter(author=user).exists():
            self.post.likes.filter(author=user).first().delete()

        else:
            Like.objects.create(author=user, post=self.post)

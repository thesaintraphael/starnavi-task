from django.db import models
from django.conf import settings

from mainapp.models import BaseModel


class Post(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    content = models.TextField()

    def __str__(self) -> str:
        return self.title

    def get_likes_count(self) -> int:
        return self.likes.all().count()

    class Meta:
        ordering = ("-id",)


class Like(BaseModel):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        ordering = ("-id",)

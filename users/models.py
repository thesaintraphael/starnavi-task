from django.db import models
from django.contrib.auth.models import AbstractUser

from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):

    activation_code = models.CharField(max_length=6, blank=True)
    reset_code = models.CharField(max_length=6, blank=True)

    last_request_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    @property
    def fullname(self) -> str:
        return self.get_full_name()

    @property
    def tokens(self) -> dict:
        refresh = RefreshToken.for_user(self)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    activation_code = models.CharField(max_length=6, blank=True)
    reset_code = models.CharField(max_length=6, blank=True)

    last_request_date = models.DateTimeField(null=True, blank=True)

    @property
    def fullname(self) -> str:
        return self.get_full_name()

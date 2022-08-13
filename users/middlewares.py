import contextlib

from django.urls import reverse
from django.utils import timezone
from rest_framework_simplejwt.tokens import AccessToken, TokenError

from .models import User


class ActivityMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):
        """Updating last_request_date field of user model if request is not made to activity endpoint"""

        jwt_token = request.headers.get("Authorization")

        if jwt_token:

            with contextlib.suppress(TokenError):
                payload = AccessToken(jwt_token.replace("Bearer ", "")).payload
                user = User.objects.get(id=payload["user_id"])

                if reverse("users:activity") not in request.path:
                    user.last_request_date = timezone.now()
                    user.save()

        return self.get_response(request)

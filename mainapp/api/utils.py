from typing import Any, Iterable
from threading import Thread

from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework import serializers


class SerializerUtil:
    def __init__(self, serializer_class) -> None:
        self.serializer_class = serializer_class

    @staticmethod
    def validate_password(password: str) -> None:
        first_isalpha = password[0].isalpha()
        if all(first_isalpha == character.isalpha() for character in password):
            raise serializers.ValidationError(
                {"password": "Password must contain at least one number and letters"}
            )

    @staticmethod
    def required(value: Any, field: str = None) -> None:
        """field is string representation of field name. Used to return error_message with key value"""

        error_message = "This field is required."

        if not value:
            if field:
                error_message = {f"{field}": error_message}

            raise serializers.ValidationError(error_message)

    def save_serializer(self, data, instance=None, context=None, **kwargs):

        serializer = self.serializer_class(
            instance=instance, data=data, context=context, **kwargs
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return serializer


class EmailUtil:
    def __init__(self, subject: str, message: str, receivers: Iterable) -> None:
        self.email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, receivers)

    def send_in_thread(self) -> None:

        Thread(target=self.email.send).start()

    def send_without_thread(self) -> None:
        self.email.send(fail_silently=False)

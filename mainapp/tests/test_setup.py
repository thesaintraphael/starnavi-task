from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model


User = get_user_model()


class TestSetup(APITestCase):
    def setUp(self) -> None:

        self.user = User.objects.create(username="testuser", email="test@mail.com")
        self.user.set_password("testpassword123")
        self.user.save()

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        return super().setUp()

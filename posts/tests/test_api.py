import json
from django.urls import reverse

from ..models import Post
from mainapp.tests.test_setup import TestSetup


POST_LIST_URL = reverse("posts:list")
POST_CREATE_URL = reverse("posts:create")
POST_DETAIL_URL = reverse("posts:detail", kwargs={"id": 1})


class TestPostAPI(TestSetup):
    def setUp(self) -> None:
        super().setUp()

        self.data = {
            "content": "Test content",
            "description": "Test description",
            "title": "Test tile",
        }

    @staticmethod
    def make_data_invlid(data: dict) -> dict:
        data["title"] = ""
        return data

    def create_post(self) -> Post:
        return Post.objects.create(author=self.user, **self.data)

    def test_unathorized_requests(self) -> None:

        client = self.client
        client.logout()
        status_codes = []

        status_codes.append(client.post(POST_CREATE_URL).status_code)
        status_codes.append(client.get(POST_LIST_URL).status_code)
        status_codes.append(client.get(POST_LIST_URL).status_code)

        self.assertEqual(status_codes.count(401), len(status_codes))

    def test_create_post_with_invalid_data(self) -> None:

        data = self.make_data_invlid(self.data.copy())

        response = self.client.post(
            POST_CREATE_URL, data=json.dumps(data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_create_post_with_valid_data(self) -> None:

        response = self.client.post(
            POST_CREATE_URL, data=json.dumps(self.data), content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

    def test_create_list_endpoint(self) -> None:

        response = self.client.get(POST_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 0)

        self.create_post()

        response = self.client.get(POST_LIST_URL)
        self.assertEqual(response.json()["count"], 1)

    def test_detail_endpoint(self) -> None:

        response = self.client.get(POST_DETAIL_URL)
        self.assertEqual(response.status_code, 404)

        self.create_post()

        response = self.client.get(POST_DETAIL_URL)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()["title"], self.data["title"])
        self.assertEqual(response.json()["content"], self.data["content"])
        self.assertEqual(response.json()["description"], self.data["description"])

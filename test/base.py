from http import HTTPStatus
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from typing import Union, List
import factory
from rest_framework.response import Response
from main.models import User
from .factories import SuperUserFactory


class TestViewSetBase(APITestCase):
    user: User = None
    client: APIClient = None
    basename: str

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = cls.create_api_user()
        cls.client = APIClient()

    @staticmethod
    def create_api_user():
        user_attributes = factory.build(dict, FACTORY_CLASS=SuperUserFactory)
        return User.objects.create(**user_attributes)

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    def create(
        self, data: dict, args: List[Union[str, int]] = None, format: str = "json"
    ) -> dict:
        self.client.force_authenticate(self.user)
        response = self.client.post(self.list_url(args), data=data, format=format)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def update(self, data: dict, id: int = None) -> dict:
        self.client.force_authenticate(self.user)
        response = self.client.patch(self.detail_url(id), data=data, format="json")
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data
    
    def request_single_resource(self, data: dict = None) -> Response:
        return self.client.get(self.list_url(), data=data)

    def single_resource(self, data: dict = None) -> dict:
        self.client.force_authenticate(self.user)
        response = self.request_single_resource(data)
        assert response.status_code == HTTPStatus.OK
        return response.data

    def request_patch_single_resource(self, attributes: dict) -> Response:
        url = self.list_url()
        return self.client.patch(url, data=attributes)

    def patch_single_resource(self, attributes: dict) -> dict:
        self.client.force_authenticate(self.user)
        response = self.request_patch_single_resource(attributes)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

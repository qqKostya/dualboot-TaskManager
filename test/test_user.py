from http import HTTPStatus

from test.base import TestViewSetBase
from test.factories import UserAvatarFactory, UserFactory, factory


class TestUserViewSet(TestViewSetBase):
    basename = "users"

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {
            **attributes,
            "id": entity["id"],
            "avatar_picture": entity["avatar_picture"],
        }

    def test_create(self):
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        user = self.create(user_attributes, format="multipart")
        expected_response = self.expected_details(user, user_attributes)
        assert user == expected_response

    def test_update(self):
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        user = self.create(user_attributes, format="multipart")
        new_data = {
            "role": "admin",
        }
        updated_attributes = dict(user, **new_data)
        expected_response = self.expected_details(user, updated_attributes)
        expected_response["avatar_picture"] = updated_attributes["avatar_picture"]
        response = self.update(new_data, user["id"])
        assert response == expected_response

    def test_large_avatar(self) -> None:
        self.client.force_authenticate(self.user)
        user_attributes = factory.build(dict, FACTORY_CLASS=UserAvatarFactory)
        response = self.client.post(
            self.list_url(), data=user_attributes, format="multipart"
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {"avatar_picture": ["Maximum size 1048576 exceeded."]}

    def test_avatar_bad_extension(self) -> None:
        self.client.force_authenticate(self.user)
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        user_attributes["avatar_picture"].name = "bad_extension.pdf"
        response = self.client.post(
            self.list_url(), data=user_attributes, format="multipart"
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {
            "avatar_picture": [
                "File extension “pdf” is not allowed. Allowed extensions are: jpeg, jpg, png."
            ]
        }

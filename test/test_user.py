from .base import TestViewSetBase
from .factories import UserFactory
from main.models.user import User
import factory


class TestUserViewSet(TestViewSetBase):
    basename = "users"

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {
            "id": entity["id"],
            "username": entity["username"],
            "email": attributes.get("email", ""),
            "first_name": attributes.get("first_name", ""),
            "last_name": attributes.get("last_name", ""),
            "role": attributes.get("role", "developer"),
        }

    def test_create(self):
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        username = user_attributes["username"]
        existing_user = User.objects.filter(username=username).first()
        if existing_user:
            existing_user.delete()

        user = self.create(user_attributes, format="multipart")
        expected_response = self.expected_details(user, user_attributes)
        assert user == expected_response

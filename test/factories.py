import factory
import faker
from main.models.user import User


class UserFactory(factory.django.DjangoModelFactory):
    username = faker.Faker(["az_AZ"])
    password = factory.PostGenerationMethodCall("set_password", "password")

    class Meta:
        model = User

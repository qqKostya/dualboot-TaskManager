import factory
from factory.django import DjangoModelFactory


from main.models.user import User


class UserFactory(DjangoModelFactory):
    username = factory.Sequence(lambda n: f"user{n}")

    class Meta:
        model = User


class SuperUserFactory(UserFactory):
    is_staff = True


class UserJWTFactory(UserFactory):
    password = factory.PostGenerationMethodCall("set_password", "password")

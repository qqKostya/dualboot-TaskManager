import factory
from faker import Faker
from django.core.files.uploadedfile import SimpleUploadedFile
from faker.providers import BaseProvider
from main.models.task import Task
from main.models.user import User
from factory.django import DjangoModelFactory


faker = Faker()


class ImageFileProvider(BaseProvider):
    def image_file(self, fmt: str = "jpeg") -> SimpleUploadedFile:
        return SimpleUploadedFile(
            self.generator.file_name(extension=fmt),
            self.generator.image(image_format=fmt),
        )


faker.add_provider(ImageFileProvider)


class UserFactory(DjangoModelFactory):
    username = factory.LazyAttribute(lambda _: faker.user_name())
    first_name = factory.LazyAttribute(lambda _: faker.first_name())
    last_name = factory.LazyAttribute(lambda _: faker.last_name())
    email = factory.LazyAttribute(lambda _: faker.unique.email())
    role = factory.LazyAttribute(
        lambda _: faker.word(
            ext_word_list=[
                "developer",
                "manager",
                "admin",
            ]
        )
    )
    date_of_birth = factory.LazyAttribute(lambda _: faker.date())
    phone = factory.LazyAttribute(lambda _: faker.unique.msisdn())
    avatar_picture = factory.LazyAttribute(lambda _: faker.unique.image_file("jpeg"))

    class Meta:
        model = User


class SuperUserFactory(UserFactory):
    is_staff = True


class UserJWTFactory(UserFactory):
    password = factory.PostGenerationMethodCall("set_password", "password")


class UserAvatarFactory(UserFactory):
    avatar_picture = SimpleUploadedFile("large.jpg", b"x" * 2 * 1024 * 1024)


class BaseTaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    title = factory.LazyAttribute(lambda _: faker.text(max_nb_chars=50))
    description = factory.LazyAttribute(lambda _: faker.text(max_nb_chars=500))
    date_change = factory.LazyAttribute(
        lambda _: faker.past_date().strftime("%Y-%m-%d")
    )
    deadline = factory.LazyAttribute(lambda _: faker.future_date().strftime("%Y-%m-%d"))
    state = factory.LazyAttribute(
        lambda _: faker.word(
            ext_word_list=[
                "new_task",
                "in_development",
                "in_qa",
                "in_code_review",
                "ready_for_release",
                "released",
                "archived",
            ]
        )
    )
    priority = factory.LazyAttribute(
        lambda _: faker.word(
            ext_word_list=[
                "Low",
                "Medium",
                "High",
            ]
        )
    )
    executor = None
    author = factory.SubFactory(UserFactory)

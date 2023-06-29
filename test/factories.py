from main.models.task import Task
import factory
from factory.django import DjangoModelFactory
from faker import Faker
from main.models import User

fake = Faker()


class UserFactory(DjangoModelFactory):
    username = factory.LazyAttribute(lambda _: fake.unique.user_name())

    class Meta:
        model = User


class SuperUserFactory(UserFactory):
    is_staff = True


class UserJWTFactory(UserFactory):
    password = factory.PostGenerationMethodCall("set_password", "password")


from faker import Faker

faker = Faker()


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

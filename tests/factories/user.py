import factory
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from factory.django import DjangoModelFactory

User = get_user_model()


class UserFactory(DjangoModelFactory):
    """Фабрика создания пользователей"""

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("email")
    password = factory.LazyFunction(lambda: make_password("pi3.1415"))

    class Meta:
        model = User

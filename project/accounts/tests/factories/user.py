from factory import Faker, SubFactory
from factory.django import DjangoModelFactory
from accounts.tests.factories.entity import EntityFactory

from accounts.models import User


class UserFactory(DjangoModelFactory):
    """User  factory."""

    class Meta:
        model = User

    company = SubFactory(EntityFactory)
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = Faker("email")
    username = Faker("email")

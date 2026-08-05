from factory import Faker

from factory.django import DjangoModelFactory


from accounts.models import Entity


class EntityFactory(DjangoModelFactory):
    """Entity  factory."""

    class Meta:
        model = Entity

    name = Faker("company")

from factory import Faker

from factory.django import DjangoModelFactory


from accounts.models import Entity


class EntityFactory(DjangoModelFactory):
    """Entity  factory."""

    class Meta:
        model = Entity

    name = Faker("company")


class SaturdayLateNightPickleballEntityFactory(EntityFactory):
    """SLNP entity factory."""

    name = "SLNP"
    logo_url = "https://assets.reclub.co/group-avatars/249506.webp"

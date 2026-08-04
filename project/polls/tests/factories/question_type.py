from factory import Faker

from factory.django import DjangoModelFactory

from polls.models import QuestionType


class QuestionTypeFactory(DjangoModelFactory):
    """Question Type factory."""

    class Meta:
        model = QuestionType

    name = Faker("name")

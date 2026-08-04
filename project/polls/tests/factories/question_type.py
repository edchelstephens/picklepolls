from factory import Faker
from factory.fuzzy import FuzzyChoice
from factory.django import DjangoModelFactory


from polls.models import QuestionType


class QuestionTypeFactory(DjangoModelFactory):
    """Question Type factory."""

    class Meta:
        model = QuestionType

    name = FuzzyChoice(choices=["Format", "Venue", "Schedule"])

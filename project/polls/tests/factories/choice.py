from factory.django import DjangoModelFactory
from factory import SubFactory
from factory import Faker
from polls.tests.factories import QuestionFactory

from polls.models import Choice


class ChoiceFactory(DjangoModelFactory):
    """Choice factory."""

    class Meta:
        model = Choice

    question = SubFactory(QuestionFactory)
    choice_text = Faker("sentence")
    votes = Faker("random_int")

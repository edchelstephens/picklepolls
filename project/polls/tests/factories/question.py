from zoneinfo import ZoneInfo

from factory.django import DjangoModelFactory
from factory import SubFactory
from factory import Faker
from polls.tests.factories import QuestionTypeFactory


from polls.models import Question


class QuestionFactory(DjangoModelFactory):
    """Question factory."""

    class Meta:
        model = Question

    question_type = SubFactory(QuestionTypeFactory)
    question_text = Faker("sentence")
    publication_datetime = Faker(
        "date_time_this_decade", tzinfo=ZoneInfo("Asia/Manila")
    )

import datetime

from django.test import TestCase
from django.utils import timezone

from polls.models import Question
from polls.tests.factories import QuestionFactory


class QuestionModelTestCase(TestCase):
    """Question model test case."""

    def setUp(self) -> None:
        """Run this setUp before each test."""
        super().setUp()
        self.future_datetime = timezone.now() + datetime.timedelta(days=30)
        self.future_question = QuestionFactory(
            publication_datetime=self.future_datetime
        )

    def test_was_published_recently_with_future_question(self) -> None:
        """Test was_published_recently() with future question should return False."""

        self.assertFalse(self.future_question.was_published_recently())

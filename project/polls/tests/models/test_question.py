import datetime

from django.test import TestCase
from django.utils import timezone

from polls.models import Question


class QuestionModelTestCase(TestCase):
    """Question model test case."""

    def setUp(self) -> None:
        """Run this setUp before each test."""
        return super().setUp()

    def test_was_published_recently_with_future_question(self) -> None:
        """Test was_published_recently() with future question should return False."""

        future_datetime = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(
            question_text="Future Question", publication_datetime=future_datetime
        )

        self.assertFalse(future_question.was_published_recently())

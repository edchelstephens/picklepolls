import datetime


from django.utils import timezone


from polls.tests.factories import QuestionFactory
from utils.tests.testcases import ModelTestCase


class QuestionModelTestCase(ModelTestCase):
    """Question model test case."""

    def setUp(self) -> None:
        """Run this setUp before each test."""
        super().setUp()

        self.question = QuestionFactory()

    def test_was_published_recently_with_future_question(self) -> None:
        """Test was_published_recently() with future question should return False."""

        future_datetime = timezone.now() + datetime.timedelta(days=30)
        self.question.publication_datetime = future_datetime
        self.question.save()
        self.question.refresh_from_db()
        self.assertFalse(self.question.was_published_recently())

    def test_was_published_recently_with_old_question(self) -> None:
        """Test was_published_recently() with old question should return False."""

        old_datetime = timezone.now() - datetime.timedelta(days=30)
        self.question.publication_datetime = old_datetime
        self.question.save()
        self.question.refresh_from_db()
        self.assertFalse(self.question.was_published_recently())

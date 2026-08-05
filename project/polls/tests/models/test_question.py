import datetime


from django.utils import timezone


from polls.tests.factories import QuestionFactory
from utils.tests.testcases import ModelTestCase


class QuestionModelTestCase(ModelTestCase):
    """Question model test case."""

    def setUp(self) -> None:
        """Run this setUp before each test."""
        super().setUp()

        self.question_text = "3rd Short Drive or 3rd Shot Drop?"
        self.question = QuestionFactory(question_text=self.question_text)

    def test_str_method(self):
        """Test string method of Question model."""
        actual = self.question.__str__()
        expected = self.question_text

        self.assertEqual(actual, expected)

    def test_repr_method(self):
        """Test repr method of Question model."""
        actual = self.question.__repr__()
        expected = f"Question(pk={self.question.pk}, question_text={self.question_text}, publication_datetime={self.question.publication_datetime})"

        self.assertEqual(actual, expected)

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

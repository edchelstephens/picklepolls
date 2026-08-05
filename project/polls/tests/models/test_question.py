import datetime


from django.utils import timezone

from utils.tests.testcases import ModelTestCase

from polls.tests.factories import QuestionFactory
from polls.tests.factories import ChoiceFactory
from polls.models import Choice


class QuestionModelTestCase(ModelTestCase):
    """Question model test case."""

    def setUp(self) -> None:
        """Run this setUp before each test."""
        super().setUp()

        self.question_text = "3rd Short Drive or 3rd Shot Drop?"
        self.question = QuestionFactory(question_text=self.question_text)

        self.choice_1_votes = 6
        self.choice_1 = ChoiceFactory(question=self.question, votes=self.choice_1_votes)

        self.choice_2_votes = 4
        self.choice_2 = ChoiceFactory(question=self.question, votes=self.choice_2_votes)

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

    def test_total_choices_returns_total_count_of_choices(self) -> None:
        """Total total_choices returns total amount of related Choice records."""
        expected = Choice.objects.filter(question=self.question).count()
        actual = self.question.total_choices

        self.assertEqual(actual, expected)

    def test_total_votes_returns_total_count_of_votes(self) -> None:
        """Total votes returns total amount of related Choice record votes."""
        expected = self.choice_1_votes + self.choice_2_votes
        actual = self.question.total_votes

        self.assertEqual(actual, expected)

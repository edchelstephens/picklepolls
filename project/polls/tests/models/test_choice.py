import datetime


from django.utils import timezone


from polls.tests.factories import ChoiceFactory
from utils.testing_utils.testcases import ModelTestCase


class ChoiceModelTestCase(ModelTestCase):
    """Choice model test case."""

    def setUp(self) -> None:
        """Run this setUp before each test."""
        super().setUp()

        self.choice_text = "Yes"
        self.votes = 6
        self.choice = ChoiceFactory(choice_text=self.choice_text, votes=self.votes)
        self.question = self.choice.question
        self.another_votes = 4
        self.another_choice = ChoiceFactory(
            question=self.question, votes=self.another_votes
        )

    def test_str_method(self) -> None:
        """Test string method of Choice model."""
        actual = self.choice.__str__()
        expected = (
            f"{self.question.question_text} - {self.choice_text} - {self.votes} votes"
        )

        self.assertEqual(actual, expected)

    def test_repr_method(self) -> None:
        """Test repr method of Choice model."""
        actual = self.choice.__repr__()
        expected = f"Choice(pk={self.choice.pk}, question_id={self.question.pk}, choice_text={self.choice_text}, votes={self.votes})"

        self.assertEqual(actual, expected)

    def test_vote_percentage(self) -> None:
        """Test vote_percentage property."""
        total_votes = self.votes + self.another_votes
        expected = round((self.votes / total_votes) * 100)
        actual = self.choice.vote_percentage

        self.assertEqual(actual, expected)

from polls.tests.factories import QuestionTypeFactory

from utils.tests.testcases import ModelTestCase


class QuestionTypeModelTest(ModelTestCase):
    """Test Question Type model."""

    def setUp(self):
        """Run this setUp before each test"""
        self.name = "Format"
        self.question_type = QuestionTypeFactory(name=self.name)

    def test_str_method(self):
        """Test string method of Question Type model."""
        actual = self.question_type.__str__()
        expected = self.name

        self.assertEqual(actual, expected)

    def test_repr_method(self):
        """Test repr method of Question Type model."""
        actual = self.question_type.__repr__()
        expected = (
            f"QuestionType(pk={self.question_type.pk}, question_type={self.name})"
        )

        self.assertEqual(actual, expected)

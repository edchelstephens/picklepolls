from django.urls import reverse
from django.utils import timezone

from polls.models.question import Question
from utils.tests.testcases import DjangoViewTestCase
from polls.tests.factories import QuestionFactory


class PollsIndexViewTestCase(DjangoViewTestCase):
    """PollsIndexView test case."""

    def setUp(self) -> None:
        """Run this setUp() before each test."""
        return super().setUp()

    def test_index_page_without_polls_published(self) -> None:
        """Test index page without questions published."""

        Question.objects.all().delete()

        response = self.client.get(reverse("polls:index"))
        question_list = response.context["question_list"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(question_list), 0)
        self.assertNotContains(response, "Vote Now")

    def test_index_page_without_polls_published(self) -> None:
        """Test index page without questions published."""

        response = self.client.get(reverse("polls:index"))
        question_list = response.context["question_list"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(question_list), 0)
        self.assertNotContains(response, "Vote Now")

    def test_index_page_with_polls_published(self) -> None:
        """Test index page with questions published."""

        question = QuestionFactory(publication_datetime=timezone.now())
        response = self.client.get(reverse("polls:index"))
        question_list = response.context["question_list"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(question_list), 1)
        self.assertContains(response, "Vote Now")

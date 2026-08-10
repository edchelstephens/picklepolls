from datetime import timedelta
from django.urls import reverse
from django.utils import timezone

import pytest


from utils.tests.testcases import DjangoViewTestCase


from polls.models.question import Question
from polls.tests.factories import QuestionFactory, ChoiceFactory


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
        self.assertIn(
            question.pk, response.context["question_list"].values_list("pk", flat=True)
        )

    def test_index_page_with_polls_future_question(self) -> None:
        """Test index page with future question."""

        question = QuestionFactory(
            publication_datetime=timezone.now() + timedelta(days=30)
        )
        response = self.client.get(reverse("polls:index"))
        question_list = response.context["question_list"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(question_list), 0)
        self.assertNotContains(response, "Vote Now")
        self.assertNotIn(
            question.pk, response.context["question_list"].values_list("pk", flat=True)
        )

    def test_index_page_with_polls_past_and_future_question(self) -> None:
        """Test index page with past and future question."""

        future_question = QuestionFactory(
            publication_datetime=timezone.now() + timedelta(days=30)
        )
        past_question = QuestionFactory(
            publication_datetime=timezone.now() - timedelta(days=1)
        )
        response = self.client.get(reverse("polls:index"))
        question_list = response.context["question_list"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(question_list), 1)
        self.assertContains(response, "Vote Now")
        self.assertNotIn(
            future_question.pk,
            response.context["question_list"].values_list("pk", flat=True),
        )
        self.assertIn(
            past_question.pk,
            response.context["question_list"].values_list("pk", flat=True),
        )

    def test_index_page_with_polls_multiple_past_questions(self) -> None:
        """Test index page with multiple past questions."""

        past_question_1 = QuestionFactory(
            publication_datetime=timezone.now() - timedelta(hours=1)
        )
        past_question_2 = QuestionFactory(
            publication_datetime=timezone.now() - timedelta(days=1)
        )
        response = self.client.get(reverse("polls:index"))
        question_list = response.context["question_list"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(question_list), 2)
        self.assertContains(response, "Vote Now")
        self.assertIn(
            past_question_1.pk,
            response.context["question_list"].values_list("pk", flat=True),
        )
        self.assertIn(
            past_question_2.pk,
            response.context["question_list"].values_list("pk", flat=True),
        )


@pytest.mark.solo
class PollVoteViewTestCase(DjangoViewTestCase):
    """PollVoteView test case."""

    def setUp(self) -> None:
        """Run this setUp() before each test."""
        super().setUp()

        self.question = QuestionFactory()
        self.choice_1_initial_votes = 0
        self.choice_1 = ChoiceFactory(
            question=self.question, votes=self.choice_1_initial_votes
        )
        self.choice_2_initial_votes = 2
        self.choice_2 = ChoiceFactory(
            question=self.question, votes=self.choice_2_initial_votes
        )

    def get_url(self, question: Question) -> str:
        """Get url."""
        return "/{}/vote/".format(question.pk)

    def test_view_adds_vote_count_on_voted_choice(self) -> None:
        """View adds given vote count on voted choice."""

        data = {"choice": self.choice_1.pk}

        self.url = self.get_url(question=self.question)

        response = self.client.post(path=self.url, data=data, follow=True)

        self.pprint_data(response)

        self.pprint_data(self.choice_1, "self.choice_1")

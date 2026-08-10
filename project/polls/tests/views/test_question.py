from datetime import timedelta
from django.urls import reverse
from django.utils import timezone

import pytest


from utils.tests.testcases import DjangoViewTestCase


from polls.models import Question, Choice
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
        self.choice_2_initial_votes = 0
        self.choice_2 = ChoiceFactory(
            question=self.question, votes=self.choice_2_initial_votes
        )
        self.choice_on_another_question_initial_votes = 0
        self.choice_on_another_question = ChoiceFactory(
            votes=self.choice_on_another_question_initial_votes
        )

    def get_url(self, question: Question) -> str:
        """Get url."""
        return "/{}/vote/".format(question.pk)

    def test_view_adds_vote_count_on_voted_choice(self) -> None:
        """View adds given vote count on voted choice."""

        data = {"choice": self.choice_1.pk}

        url = self.get_url(question=self.question)

        votes_before = sum(Choice.objects.values_list("votes", flat=True))

        response = self.client.post(path=url, data=data, follow=True)

        votes_after = sum(Choice.objects.values_list("votes", flat=True))

        self.choice_1.refresh_from_db()

        self.assertTrue(response.status_code, 200)
        self.assertGreater(votes_after, votes_before)
        self.assertEqual(votes_before + 1, votes_after)
        self.assertGreater(self.choice_1.votes, self.choice_1_initial_votes)

    def test_view_adds_no_vote_count_on_non_voted_choice(self) -> None:
        """View adds given vote count on non voted choice."""

        data = {"choice": self.choice_on_another_question.pk}

        url = self.get_url(question=self.question)

        votes_before = sum(Choice.objects.values_list("votes", flat=True))

        response = self.client.post(path=url, data=data, follow=True)

        votes_after = sum(Choice.objects.values_list("votes", flat=True))

        self.choice_on_another_question.refresh_from_db()

        self.assertTrue(response.status_code, 200)
        self.assertEqual(votes_after, votes_before)
        self.assertEqual(
            self.choice_on_another_question.votes,
            self.choice_on_another_question_initial_votes,
        )

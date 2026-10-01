import pytest

from accounts.tests.factories import EntityFactory, UserFactory

from accounts.models import User
from polls.models import Question, Choice
from polls.serializers import QuestionSerializer
from polls.tests.factories import QuestionFactory, QuestionTypeFactory, ChoiceFactory
from api.views.polls import (
    QuestionAPIView,
    QuestionsAPIView,
    PublicQuestionsAPIView,
    PublicQuestionAPIView,
    PublicQuestionVoteAPIView,
)

from utils.testing_utils.testcases import RestAPITestCase



class PublicQuestionVoteAPIViewTestCase(RestAPITestCase):
    """PublicQuestionVoteAPIView test case."""

    def setUp(self) -> None:
        """Run this setUp before each test."""
        super().setUp()
        self.request_factory = self.get_request_factory()
        self.view = PublicQuestionVoteAPIView.as_view()
        self.question = QuestionFactory()
        self.url = self.get_url(question_id=self.question.pk)
        self.choice_1_initial_votes = 0
        self.choice_1 = ChoiceFactory(
            question=self.question, votes=self.choice_1_initial_votes
        )

    def get_url(self, question_id: int) -> str:
        """Get url."""

        url = f"/api/public/question/{question_id}/vote/"
        return url

    def test_POST_request_increments_votes_for_choice(self) -> None:
        """POST request increments votes for choice."""

        data = {"choice": self.choice_1.pk}

        request = self.request_factory.post(
            self.url, data=data, content_type="application/json"
        )
        response = self.view(request, pk=self.question.pk)

        response_data = response.data

        self.pprint_response(response_data)

        updated_choice = Choice.objects.get(pk=self.choice_1.pk)
        updated_choice.refresh_from_db()

        expected_title = "Success"
        expected_message = "Voted on question."

        self.assertNotEqual(updated_choice.votes, self.choice_1_initial_votes)
        self.assertEqual(updated_choice.votes, self.choice_1_initial_votes + 1)

        self.assertEqual(response_data["title"], expected_title)
        self.assertEqual(response_data["message"], expected_message)


class QuestionsAPIViewTestCase(RestAPITestCase):
    """QuestionsAPIView test case."""

    def setUp(self) -> None:
        """Run this setUp before each test."""
        super().setUp()
        self.request_factory = self.get_request_factory()
        self.view = QuestionsAPIView.as_view()
        self.url = "/api/polls/questions/"
        self.user = UserFactory()
        self.questions = [
            QuestionFactory(author=self.user),
            QuestionFactory(author=self.user),
            QuestionFactory(author=self.user),
        ]
        self.another_user = UserFactory()
        self.questions_by_another_user = [
            QuestionFactory(author=self.another_user),
            QuestionFactory(author=self.another_user),
        ]

    def get_expected_data(self, author: User) -> dict:
        """Get expected data."""

        questions = Question.objects.filter(author=author)
        serializer = QuestionSerializer(questions, many=True)
        serializer_data = serializer.data

        data = {
            "data": serializer_data,
            "count": len(serializer_data),
        }

        return data

    def test_get_request_returns_all_questions_authored_by_user(self) -> None:
        """GET request returns all questions authored by user."""

        request = self.request_factory.get(self.url)
        self.set_user(request=request, user=self.user)

        response = self.view(request)
        response_data = response.data

        expected_data = self.get_expected_data(author=self.user)

        self.assertEqual(response_data["count"], len(self.questions))
        self.assertEqual(response_data, expected_data)


class QuestionAPIViewTestCase(RestAPITestCase):
    """QuestionAPIView test case."""

    def setUp(self) -> None:
        """Run this setUp before each test."""
        super().setUp()
        self.request_factory = self.get_request_factory()
        self.view = QuestionAPIView.as_view()
        self.url = "/api/polls/question/"
        self.user = UserFactory()
        self.entity = EntityFactory(owner=self.user)
        self.question_type = QuestionTypeFactory()

    def test_post_request_creates_questions_with_choices_given_on_payload(self) -> None:
        """Post request creates questions with choices on given payload."""

        choice_text_1 = "BounZ"
        choice_text_2 = "Dula"
        choices = [choice_text_1, choice_text_2]
        data = {
            "question_type": self.question_type.pk,
            "question_text": "What is the best pickleball court in CDO Uptown?",
            "choices": choices,
        }

        request = self.request_factory.post(
            path=self.url, data=data, content_type="application/json"
        )
        self.set_user(request=request, user=self.user)

        response = self.view(request)
        response_data = response.data

        question_id = response_data["id"]
        question_created = Question.objects.get(pk=question_id)

        self.assertEqual(question_created.author, self.user)
        self.assertEqual(question_created.entity, self.entity)
        self.assertTrue(
            Choice.objects.filter(
                question=question_created, choice_text=choice_text_1
            ).exists()
        )
        self.assertTrue(
            Choice.objects.filter(
                question=question_created, choice_text=choice_text_2
            ).exists()
        )
        self.assertEqual(
            Choice.objects.filter(question=question_created).count(), len(choices)
        )

    def test_delete_properly_deletes_question_authored_by_user(self) -> None:
        """Delete request deletes question authored by user."""

        question = QuestionFactory(author=self.user)
        question_id = int(question.pk)

        request = self.request_factory.delete(self.url)
        self.set_user(request=request, user=self.user)

        response = self.view(request, pk=question_id)
        response_data = response.data

        expected_message = "Question deleted."
        self.assertEqual(response_data["message"], expected_message)
        self.assertFalse(Question.objects.filter(pk=question_id).exists())

    def test_delete_prevents_user_from_deleting_a_question_he_is_not_the_author_of(
        self,
    ) -> None:
        """Delete prevents user from deleting a question he is not the author of."""

        another_user = UserFactory()
        question = QuestionFactory(author=another_user)
        question_id = int(question.pk)

        request = self.request_factory.delete(self.url)
        self.set_user(request=request, user=self.user)

        response = self.view(request, pk=question_id)
        response_data = response.data

        expected_message = "Question does not exist"
        self.assertEqual(response_data["message"], expected_message)
        self.assertTrue(Question.objects.filter(id=question_id).exists())


class PublicQuestionAPIViewTestCase(RestAPITestCase):
    """PublicQuestionAPIView test case."""

    def setUp(self) -> None:
        """Run this setUp before each test."""
        super().setUp()
        self.request_factory = self.get_request_factory()
        self.view = PublicQuestionAPIView.as_view()
        self.question = QuestionFactory()
        self.url = self.get_url(question_id=self.question.pk)

    def get_url(self, question_id) -> str:
        """Get url."""

        url = f"/api/public/question/{question_id}/"
        return url

    def test_get_request_returns_question_data(self) -> None:
        """Get request returns question data."""

        request = self.request_factory.get(self.url)
        response = self.view(request, pk=self.question.pk)
        response_data = response.data

        expected_data = self.question.get_data()

        self.assertEqual(response_data, expected_data)

    def test_get_request_returns_404_if_question_does_not_exists(self) -> None:
        """GET request on non existing question returns 404."""

        non_existing_question_id = 9_999_999_999
        url = self.get_url(question_id=non_existing_question_id)

        request = self.request_factory.get(url)
        response = self.view(request, pk=non_existing_question_id)

        response_data = response.data

        expected_message = "Question not found"

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data["message"], expected_message)


class PublicQuestionsAPIViewTestCase(RestAPITestCase):
    """PublicQuestionsAPIView test case."""

    def setUp(self) -> None:
        """Run this setUp before each test."""
        super().setUp()
        self.request_factory = self.get_request_factory()
        self.view = PublicQuestionsAPIView.as_view()
        self.url = "/api/public/questions/"
        self.active_questions = [
            QuestionFactory(),
            QuestionFactory(),
            QuestionFactory(),
        ]
        self.in_active_question = QuestionFactory(is_active=False)

    def get_expected_data(self) -> dict:
        """Get expected data."""

        questions = Question.objects.filter(is_active=True)
        serializer = QuestionSerializer(questions, many=True)
        serializer_data = serializer.data

        data = {"data": serializer_data, "count": len(serializer_data)}

        return data

    def test_get_request_returns_all_active_questions(self) -> None:
        """Get request returns all active questions."""

        request = self.request_factory.get(self.url)
        response = self.view(request)
        response_data = response.data

        response_questions_ids = [question["id"] for question in response_data["data"]]

        expected_data = self.get_expected_data()

        self.assertEqual(response_data, expected_data)
        self.assertEqual(response_data["count"], len(self.active_questions))
        self.assertNotIn(self.in_active_question.pk, response_questions_ids)

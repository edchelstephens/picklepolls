import pytest

from accounts.tests.factories import EntityFactory, UserFactory
from polls.models import Question, Choice
from polls.tests.factories import QuestionTypeFactory
from api.views.polls import QuestionAPIView, QuestionsAPIView

from utils.testing_utils.testcases import RestAPITestCase


@pytest.mark.solo
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

import pytest

from polls.tests.factories import QuestionFactory, ChoiceFactory
from polls.serializers.choice import ChoiceSerializer
from polls.models import Choice

from api.views.polls import PublicChoicesAPIView

from utils.testing_utils.testcases import RestAPITestCase


class PublicChoicesAPIViewTestCase(RestAPITestCase):
    """PublicChoicesAPIView test case."""

    def setUp(self) -> None:
        """Run this setUp before each test."""
        super().setUp()
        self.request_factory = self.get_request_factory()
        self.view = PublicChoicesAPIView.as_view()
        self.url = "/api/public/choices/"
        self.question = QuestionFactory()
        self.choices = [
            ChoiceFactory(question=self.question),
            ChoiceFactory(question=self.question),
            ChoiceFactory(question=self.question),
        ]
        self.inactive_question = QuestionFactory(is_active=False)
        self.inactive_question_choices = [
            ChoiceFactory(question=self.inactive_question)
        ]

    def get_expected_data(self) -> dict:
        """Get expected data."""

        choices = Choice.objects.filter(question__is_active=True)
        serializer = ChoiceSerializer(choices, many=True)

        serializer_data = serializer.data

        data = {"data": serializer_data, "count": len(serializer_data)}

        return data

    def test_get_request_resturns_active_question_choices_data(self) -> None:
        """GET request returns active question choices data."""

        request = self.request_factory.get(self.url)
        response = self.view(request)
        response_data = response.data

        expected_data = self.get_expected_data()

        self.assertEqual(response_data["count"], len(self.choices))
        self.assertEqual(response_data, expected_data)

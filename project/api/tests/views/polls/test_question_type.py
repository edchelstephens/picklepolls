import pytest

from api.views.polls import PublicQuestionTypesAPIView

from polls.tests.factories import QuestionTypeFactory
from polls.serializers.question_type import QuestionTypeSerializer
from polls.models import QuestionType

from utils.testing_utils.testcases import RestAPITestCase


class PublicQuestionTypesAPIViewTestCase(RestAPITestCase):
    """PublicQuestionTypesAPIView test case."""

    def setUp(self) -> None:
        """Run this setUp before each test."""
        super().setUp()
        self.request_factory = self.get_request_factory()
        self.view = PublicQuestionTypesAPIView.as_view()
        self.url = "/api/public/question_types/"
        self.question_types = [
            QuestionTypeFactory(),
            QuestionTypeFactory(),
            QuestionTypeFactory(),
        ]

    def get_expected_data(self) -> dict:
        """Get expected data."""

        question_types = QuestionType.objects.all()
        serializer = QuestionTypeSerializer(question_types, many=True)
        serializer_data = serializer.data

        data = {
            "data": serializer_data,
            "count": len(serializer_data),
        }

        return data

    def test_get_returns_all_question_types_data(self) -> None:
        """GET request returns all question types data."""

        request = self.request_factory.get(self.url)
        response = self.view(request)
        response_data = response.data

        expected_data = self.get_expected_data()

        self.assertEqual(response_data, expected_data)
        self.assertEqual(response_data["count"], len(self.question_types))

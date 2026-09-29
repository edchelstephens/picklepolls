import pytest

from django.db.models import QuerySet

from utils.testing_utils.testcases import RestAPITestCase
from api.views.accounts import PublicEntitiesAPIView

from accounts.serializers import EntitySerializer
from accounts.models import Entity
from accounts.tests.factories import EntityFactory

# urlpatterns = [
#     path("accounts/login/", TokenAPIView.as_view()),
#     path("accounts/entities/", EntitiesAPIView.as_view()),
#     path("polls/question/", QuestionAPIView.as_view()),
#     path("polls/questions/", QuestionsAPIView.as_view()),
#     path("polls/question/<int:pk>/", QuestionAPIView.as_view()),
#     path("public/entities/", PublicEntitiesAPIView.as_view()),
#     path("public/question_types/", PublicQuestionTypesAPIView.as_view()),
#     path("public/choices/", PublicChoicesAPIView.as_view()),
#     path("public/questions/", PublicQuestionsAPIView.as_view()),
#     path("public/question/<int:pk>/", PublicQuestionAPIView.as_view()),
#     path("public/question/<int:pk>/vote/", PublicQuestionVoteAPIView.as_view()),
# ]


@pytest.mark.solo
class PublicEntitiesAPIViewTestCase(RestAPITestCase):
    """PublicEntitiesAPIView test case."""

    def setUp(self) -> None:
        """Run this setUp before each test."""
        super().setUp()
        self.view = PublicEntitiesAPIView.as_view()
        self.url = "/api/public/entities/"
        self.request_factory = self.get_request_factory()
        self.entity_1 = EntityFactory()
        self.entity_2 = EntityFactory()

    def get_expected_data(self, entities: QuerySet) -> dict:
        """Get expected data."""

        serializer = EntitySerializer(entities, many=True)
        serializer_data = serializer.data

        data = {"data": serializer_data, "count": len(serializer_data)}

        return data

    def test_get_request_returns_entities_data(self) -> None:
        """Get request returns entities data."""

        request = self.request_factory.get(self.url)

        response = self.view(request)
        response_data = response.data

        entities = Entity.objects.all()

        expected_data = self.get_expected_data(entities=entities)

        self.assertEqual(expected_data, response_data)

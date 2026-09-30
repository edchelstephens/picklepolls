import pytest

from django.db.models import QuerySet, Q

from utils.testing_utils.testcases import RestAPITestCase

from accounts.serializers import EntitySerializer
from accounts.models import Entity, User
from accounts.tests.factories import EntityFactory, UserFactory


from api.views.accounts import PublicEntitiesAPIView, EntitiesAPIView


class EntityAPIVIewsTestCase(RestAPITestCase):
    """Entities api endpoints test cases."""

    def setUp(self) -> None:
        """Run this setUp before each test."""
        super().setUp()
        self.request_factory = self.get_request_factory()
        self.user_1 = UserFactory()
        self.user_2 = UserFactory()

        self.entity_1 = EntityFactory(owner=self.user_1)
        self.entity_2 = EntityFactory(owner=self.user_2)

    def get_expected_data(self, entities: QuerySet) -> dict:
        """Get expected data."""

        serializer = EntitySerializer(entities, many=True)
        serializer_data = serializer.data

        data = {"data": serializer_data, "count": len(serializer_data)}

        return data


class EntitiesAPIViewTestCase(EntityAPIVIewsTestCase):
    """EntitiesAPIView test case."""

    def setUp(self) -> None:
        """Run this setUp before each test."""
        super().setUp()
        self.view = EntitiesAPIView.as_view()
        self.url = "/api/accounts/entities/"

    def test_get_request_only_returns_entities_owned_by_user_or_where_user_is_part_of_entity_admins(
        self,
    ) -> None:
        """Get request returns expected data."""

        request = self.request_factory.get(self.url)
        self.set_user(request=request, user=self.user_1)
        response = self.view(request)
        response_data = response.data

        entities_filters = Q(owner=self.user_1) | Q(admins=self.user_1)
        entities = Entity.objects.filter(entities_filters)
        expected_data = self.get_expected_data(entities=entities)

        self.assertEqual(response_data, expected_data)


class PublicEntitiesAPIViewTestCase(EntityAPIVIewsTestCase):
    """PublicEntitiesAPIView test case."""

    def setUp(self) -> None:
        """Run this setUp before each test."""
        super().setUp()
        self.view = PublicEntitiesAPIView.as_view()
        self.url = "/api/public/entities/"

    def test_get_request_returns_entities_data(self) -> None:
        """Get request returns entities data."""

        request = self.request_factory.get(self.url)

        response = self.view(request)
        response_data = response.data

        entities = Entity.objects.all()

        expected_data = self.get_expected_data(entities=entities)

        self.assertEqual(response_data, expected_data)

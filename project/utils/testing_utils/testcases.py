import datetime
import time
import json
from typing import Any, List, Optional
from urllib.parse import urlencode

import pytest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.db.models import Model, QuerySet
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.test.testcases import SimpleTestCase, TestCase

from rest_framework.test import APITestCase, force_authenticate

from accounts.models import User

from utils.debug import DebuggerMixin
from utils.testing_utils.request import (
    DjangoRequestFactoryMixin,
    RestRequestFactoryMixin,
)


class TestMixin(DebuggerMixin):
    """Mixin class for tests."""

    def save_and_refresh(self, model: Model) -> Model:
        """Save and refresh from db the model instance and return it."""
        model.save()
        model.refresh_from_db()

        return model


@pytest.mark.django_db
@pytest.mark.models
class QuerySetTestMixin(TestMixin):
    """Mixin for query set tests."""

    def assertQuerySetEqualByIds(
        self, first: QuerySet, second: QuerySet, msg: Optional[str] = None
    ) -> None:
        """Assert query sets are equal by using id checks."""
        first_queryset_ids = list(first.order_by("id").values_list("id", flat=True))
        second_queryset_ids = list(second.order_by("id").values_list("id", flat=True))

        if msg is None:
            msg = "Queryset ids not equal! {} != {}".format(
                repr(first_queryset_ids), repr(second_queryset_ids)
            )
        assert first_queryset_ids == second_queryset_ids, msg

    def assertQuerySetIsIn(
        self, first: QuerySet, second: QuerySet, msg: Optional[str] = None
    ) -> None:
        """Assert first query sets is a subset of second queryset."""
        first_queryset_ids = list(first.values_list("id", flat=True))
        second_queryset_ids = list(second.values_list("id", flat=True))

        if msg is None:
            msg = "Queryset {} not in {}!".format(
                repr(first_queryset_ids), repr(second_queryset_ids)
            )
        for model_id in first_queryset_ids:
            assert model_id in second_queryset_ids, msg


@pytest.mark.non_db
class NonDBTestCase(SimpleTestCase):
    """Our custom test case wrapper for tests not involving database access."""

    maxDiff = None


@pytest.mark.django_db
class WithDBTestCase(QuerySetTestMixin, TestCase):
    """Our custom test case wrapper for tests including database access."""

    maxDiff = None


@pytest.mark.django_db
@pytest.mark.models
class ModelTestCase(TestMixin, TestCase):
    """Our custom test case wrapper for testing django models."""

    maxDiff = None


@pytest.mark.django_db
@pytest.mark.django_views
class DjangoViewTestCase(TestMixin, DjangoRequestFactoryMixin, TestCase):
    """Our test case wrapper for testing django views."""

    maxDiff = None

    def set_user(self, request, user) -> None:
        """Manually set request.user to user.

        To simulate a user logged-in trying to access an endpoint.
        """
        request.user = user

    def get_json_response_data(self, response) -> Any:
        """Get json response data from JSONResponse object content."""
        try:
            return json.loads(response.content)
        except TypeError as exc:  # noqa
            return json.loads(self.get_string_response(response))
        except Exception as exc:
            raise exc

    def get_dict_response_data(self, response) -> dict:
        """Get expected dictionary response data from deserialized JSONResponse response.content."""
        data = self.get_json_response_data(response)
        if not isinstance(data, dict):
            raise TypeError(
                "deserialized response.content is not a python dict but a {}".format(
                    type(data)
                )
            )
        return data

    def get_list_response_data(self, response) -> list:
        """Get expected list response data from deserialized JSONResponse response.content."""
        data = self.get_json_response_data(response)
        if not isinstance(data, list):
            raise TypeError(
                "deserialized response.content is not a python list but a {}".format(
                    type(data)
                )
            )
        return data

    def get_string_response(self, response) -> str:
        """Get the decoded response string from bytestring response.content."""
        return response.content.decode()


@pytest.mark.django_db
@pytest.mark.api_views
class RestAPITestCase(TestMixin, RestRequestFactoryMixin, APITestCase):
    """Our test case wrapper for rest_framework api views."""

    maxDiff = None

    def set_user(self, request, user: User) -> None:
        """Forcibly set request.user to user.

        This is used on views which requires authenticated requests.
        https://www.django-rest-framework.org/api-guide/testing/#forcing-authentication
        """
        force_authenticate(request, user=user)
        request.user = user

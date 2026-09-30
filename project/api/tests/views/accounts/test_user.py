import pytest

from rest_framework.authtoken.models import Token
from accounts.models import User
from accounts.tests.factories import UserFactory

from utils.testing_utils.testcases import RestAPITestCase
from api.views.accounts.user import TokenAPIView


@pytest.mark.solo
class TokenAPIViewTestCase(RestAPITestCase):
    """TokenAPIView test case."""

    def setUp(self) -> None:
        """Run this setUp before each test."""
        super().setUp()
        self.request_factory = self.get_request_factory()

        self.view = TokenAPIView.as_view()
        self.url = "/api/accounts/login/"
        self.email = "tester@picklepolls.com"
        self.password = "password@1234"
        self.user = UserFactory()
        self.user.email = self.email
        self.user.set_password(self.password)
        self.user.save()
        self.user.refresh_from_db()

    def get_expected_data(self, user: User) -> dict:
        """Get expected data."""

        token, is_created = Token.objects.get_or_create(user=user)

        data = {"id": user.pk, "token": token.key, "email": user.email}

        return data

    def test_post_request_with_correct_credentials_returns_user_token(self) -> None:
        """Test post request with correct cerdentials returns token."""

        data = {"email": self.email, "password": self.password}

        request = self.request_factory.post(
            path=self.url, data=data, content_type="application/json"
        )
        response = self.view(request)

        response_data = response.data

        self.pprint_response(response_data)

        expected_data = self.get_expected_data(user=self.user)

        self.assertEqual(response_data, expected_data)

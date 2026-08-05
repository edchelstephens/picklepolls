import datetime


from django.utils import timezone


from accounts.tests.factories import UserFactory
from utils.tests.testcases import ModelTestCase


class UserModelTestCase(ModelTestCase):
    """User model test case."""

    def setUp(self) -> None:
        """Run this setUp before each test."""
        super().setUp()
        self.profile_pic_url = "https://avatars.githubusercontent.com/u/49672830?v=4"
        self.email = "pickler@gmail.com"
        self.first_name = "Pickle"
        self.last_name = "Baller"
        self.user = UserFactory(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            profile_pic_url=self.profile_pic_url,
        )

    def test_str_method(self):
        """Test string method."""
        actual = self.user.__str__()
        expected = f"{self.user.first_name} {self.user.last_name}"

        self.assertEqual(actual, expected)

    def test_repr_method(self):
        """Test repr method."""
        actual = self.user.__repr__()
        expected = f"User(pk={self.user.pk}, email={self.email})"

        self.assertEqual(actual, expected)

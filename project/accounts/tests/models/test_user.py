import datetime


from django.utils import timezone


from accounts.tests.factories import UserFactory
from utils.testing_utils.testcases import ModelTestCase


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

    def test_has_image_returns_True_with_User_having_profile_pic_url(self) -> None:
        """Test has_image() property returns True with User having profile pic url filled."""
        self.assertTrue(self.user.has_image)

    def test_has_image_returns_False_on_no_profile_pic_url(self) -> None:
        """Test has_image() property returns False on User not having profile pic url filled."""
        self.user.profile_pic_url = ""
        self.user.save()
        self.user.refresh_from_db()
        self.assertFalse(self.user.has_image)

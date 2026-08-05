from accounts.tests.factories import EntityFactory

from utils.tests.testcases import ModelTestCase


class EntityModelTest(ModelTestCase):
    """Test Question Type model."""

    def setUp(self):
        """Run this setUp before each test"""
        self.name = "Aces"
        self.logo_url = "https://assets.reclub.co/group-avatars/154681.webp"
        self.entity = EntityFactory(name=self.name, logo_url=self.logo_url)

    def test_str_method(self):
        """Test string method of Question Type model."""
        actual = self.entity.__str__()
        expected = self.name

        self.assertEqual(actual, expected)

    def test_repr_method(self):
        """Test repr method of Question Type model."""
        actual = self.entity.__repr__()
        expected = f"Entity(pk={self.entity.pk}, name={self.name})"

        self.assertEqual(actual, expected)

    def test_has_image_returns_True_with_entity_having_logo_url(self) -> None:
        """Test has_image() property returns True wih entity haveing logo url filled."""
        self.assertTrue(self.entity.has_image)

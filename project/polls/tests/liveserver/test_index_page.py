from utils.tests.testcases import DjangoStaticLiveServerTestCase

import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options

from polls.tests.factories import QuestionFactory, ChoiceFactory


@pytest.mark.liveserver
class IndexSeleniumTestCase(DjangoStaticLiveServerTestCase):
    """Index page selenium test case."""

    @classmethod
    def setUpClass(cls):
        """setUpClass."""
        super().setUpClass()
        options = Options()
        options.add_argument("--start-maximized")
        cls.selenium = WebDriver(options=options)
        cls.selenium.implicitly_wait(time_to_wait=10)

        cls.question_1 = QuestionFactory()
        cls.choice_1 = ChoiceFactory(question=cls.question_1)
        cls.choice_2 = ChoiceFactory(question=cls.question_1)

    @classmethod
    def tearDownClass(cls):
        """tearDownClass."""
        cls.selenium.quit()
        super().tearDownClass()

    def test_index_page(self) -> None:
        """Test index page."""
        self.selenium.get(f"{self.live_server_url}/")

        header = self.selenium.find_element(By.ID, "header-app-name")
        expected_header_title = "PicklePolls"

        self.assertEqual(header.text, expected_header_title)

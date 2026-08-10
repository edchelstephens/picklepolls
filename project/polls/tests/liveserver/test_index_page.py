from optparse import Option
import os
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service


from utils.testing_utils.testcases import DjangoStaticLiveServerTestCase

from polls.models import Choice, Question
from polls.tests.factories import QuestionFactory, ChoiceFactory

from accounts.tests.factories.entity import SaturdayLateNightPickleballEntityFactory


@pytest.mark.liveserver
class IndexSeleniumTestCase(DjangoStaticLiveServerTestCase):
    """Index page selenium test case."""

    @classmethod
    def get_options(cls) -> Options:
        """Get options instance."""
        options = Options()
        if os.getenv("CICD"):
            options.add_argument("--headless")
        return options

    @classmethod
    def get_webdriver(cls, options: Options) -> WebDriver:
        """Get webdriver."""

        if os.getenv("CICD"):
            service = Service(
                executable_path=os.path.join(
                    os.environ["GECKOWEBDRIVER"],
                    "geckodriver",
                )
            )
            webdriver = WebDriver(service=service, options=options)

        else:
            webdriver = WebDriver(options=options)

        return webdriver

    @classmethod
    def setUpClass(cls):
        """setUpClass."""
        super().setUpClass()

        options = cls.get_options()
        cls.selenium = cls.get_webdriver(options=options)
        cls.selenium.implicitly_wait(time_to_wait=10)

        if not os.getenv("CICD"):
            cls.selenium.maximize_window()

    @classmethod
    def tearDownClass(cls):
        """tearDownClass."""
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self) -> None:
        """Run this setUp before each test."""
        super().setUp()
        self.entity = SaturdayLateNightPickleballEntityFactory()
        self.question_1 = QuestionFactory(entity=self.entity)
        self.choice_1 = ChoiceFactory(question=self.question_1, votes=1)
        self.choice_2 = ChoiceFactory(question=self.question_1, votes=1)

    def test_index_page_has_expected_header(self) -> None:
        """Test index page displays header text."""
        self.selenium.get(f"{self.live_server_url}/")

        self.pause(seconds=2)
        header = self.selenium.find_element(By.ID, "header-app-name")
        expected_header_title = "PicklePolls"

        self.assertEqual(header.text, expected_header_title)

    def test_index_page_has_vote_now_button_given_that_there_is_a_published_question(
        self,
    ) -> None:
        """Test index page has vote now button given taht there is a published question."""
        self.selenium.get(f"{self.live_server_url}/")

        self.pause(seconds=2)

        vote_link_id = f"vote-on-poll-{self.question_1.pk}"
        vote_link = self.selenium.find_element(By.ID, vote_link_id)

        self.assertTrue(Question.objects.exists())
        self.assertTrue(Choice.objects.exists())
        self.assertIn("Vote Now", vote_link.text)

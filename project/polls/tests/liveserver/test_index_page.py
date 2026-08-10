import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options


from utils.testing_utils.testcases import DjangoStaticLiveServerTestCase

from polls.models import Choice, Question
from polls.tests.factories import QuestionFactory, ChoiceFactory

from accounts.tests.factories.entity import SaturdayLateNightPickleballEntityFactory


@pytest.mark.skip_on_ci
@pytest.mark.liveserver
class IndexSeleniumTestCase(DjangoStaticLiveServerTestCase):
    """Index page selenium test case."""

    def get_chrome_options(self) -> Options:
        """Get chrome driver options."""
        options = Options()
        options.add_argument("--start-maximized")

    @classmethod
    def setUpClass(cls):
        """setUpClass."""
        super().setUpClass()

        cls.selenium = WebDriver()
        cls.selenium.maximize_window()
        cls.selenium.implicitly_wait(time_to_wait=10)

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

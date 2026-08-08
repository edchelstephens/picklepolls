from utils.tests.testcases import DjangoStaticLiveServerTestCase

import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options

from polls.tests.factories import QuestionFactory, ChoiceFactory
from polls.models import Choice, Question
from accounts.tests.factories.entity import SaturdayLateNightPickleballEntityFactory


@pytest.mark.liveserver
class IntegrationTestIndexToVotingToResultsSeleniumTestCase(
    DjangoStaticLiveServerTestCase
):
    """Integration test from index to voting to results page selenium test case."""

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
        self.choice_1 = ChoiceFactory(question=self.question_1)
        self.choice_2 = ChoiceFactory(question=self.question_1)

    def test_voting_on_an_choice_updates_the_poll_results(
        self,
    ) -> None:
        """Voting on a choice updates poll results."""
        self.selenium.get(f"{self.live_server_url}/")

        vote_link_id = f"vote-on-poll-{self.question_1.pk}"
        vote_link = self.selenium.find_element(By.ID, vote_link_id)

        self.pause(seconds=3)

        vote_link.click()

        self.pause(seconds=3)

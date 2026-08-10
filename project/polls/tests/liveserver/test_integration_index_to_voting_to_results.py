import os


import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options

from polls.tests.factories import QuestionFactory, ChoiceFactory
from polls.models import Choice, Question
from accounts.tests.factories.entity import SaturdayLateNightPickleballEntityFactory
from utils.testing_utils.testcases import DjangoStaticLiveServerTestCase


@pytest.mark.liveserver
class IntegrationTestIndexToVotingToResultsSeleniumTestCase(
    DjangoStaticLiveServerTestCase
):
    """Integration test from index to voting to results page selenium test case."""

    @classmethod
    def get_options(cls) -> Options:
        """Get options instance."""
        options = Options()
        if os.getenv("CICD"):
            options.add_argument("--headless")
        return options

    @classmethod
    def setUpClass(cls):
        """setUpClass."""
        super().setUpClass()

        options = cls.get_options()
        cls.selenium = WebDriver(options=options)
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

        self.choice_1_initial_votes = 1
        self.choice_1 = ChoiceFactory(
            question=self.question_1, votes=self.choice_1_initial_votes
        )

        self.choice_2_initial_votes = 1
        self.choice_2 = ChoiceFactory(
            question=self.question_1, votes=self.choice_2_initial_votes
        )
        self.votes_before = sum(Choice.objects.values_list("votes", flat=True))

    def test_voting_on_an_choice_updates_the_poll_results(
        self,
    ) -> None:
        """Voting on a choice updates poll results."""

        self.selenium.get(f"{self.live_server_url}/")

        self.pause(seconds=2)

        vote_link_id = f"vote-on-poll-{self.question_1.pk}"
        vote_link = self.selenium.find_element(By.ID, vote_link_id)
        vote_link.click()

        self.pause(seconds=2)

        choice_radio_button_id = f"choice-{self.choice_1.pk}"
        choice_button = self.selenium.find_element(By.ID, choice_radio_button_id)
        choice_button.click()

        self.pause(seconds=2)

        submit_button = self.selenium.find_element(
            By.CSS_SELECTOR, 'button[type="submit"]'
        )
        submit_button.click()
        self.pause(seconds=2)

        votes_after = sum(Choice.objects.values_list("votes", flat=True))

        self.choice_1.refresh_from_db()
        choice_1_votes_after = int(self.choice_1.votes)

        self.assertGreater(choice_1_votes_after, self.choice_1_initial_votes)
        self.assertEqual(self.choice_1_initial_votes + 1, choice_1_votes_after)

        expected_votes = self.choice_1_initial_votes + self.choice_2_initial_votes + 1
        expected_text = f"{expected_votes} total responses logged"

        self.assertIn(expected_text, self.selenium.page_source)
        self.assertEqual(expected_votes, votes_after)

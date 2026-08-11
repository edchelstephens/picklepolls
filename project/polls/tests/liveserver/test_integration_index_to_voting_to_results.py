import os


import pytest

from selenium.webdriver.common.by import By


from polls.tests.factories import QuestionFactory, ChoiceFactory
from polls.models import Choice, Question
from accounts.tests.factories.entity import SaturdayLateNightPickleballEntityFactory


from utils.testing_utils.liveserver_testcases import DjangoStaticLiveServerTestCase


@pytest.mark.liveserver
class IntegrationTestIndexToVotingToResultsSeleniumTestCase(
    DjangoStaticLiveServerTestCase
):
    """Integration test from index to voting to results page selenium test case."""

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

        self.choice_1_initial_votes = 1
        self.choice_1 = ChoiceFactory(
            question=self.question_1, votes=self.choice_1_initial_votes
        )

        self.choice_2_initial_votes = 1
        self.choice_2 = ChoiceFactory(
            question=self.question_1, votes=self.choice_2_initial_votes
        )
        self.votes_before = sum(Choice.objects.values_list("votes", flat=True))

    def pluralize(self, count: int, text: str) -> str:
        """Pluralize text based on count int value."""

        return text + "s" if count != 1 else text

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

        winning_choice_p_element = self.selenium.find_element(
            By.ID, "winning-choice-text"
        )

        expected_winning_choice_p_element_text = self.choice_1.choice_text + " 🎉"
        winning_choice_span_element_on_breakdown = self.selenium.find_element(
            By.ID, "winning-choice-text-on-breakdown"
        )

        winning_choice_votes_on_breakdown_span_element = self.selenium.find_element(
            By.ID, "winning-choice-votes-on-breakdown"
        )

        expected_winning_votes_text = f"{self.choice_1.votes} {self.pluralize(count=self.choice_1.votes, text='vote')}"

        self.assertEqual(
            winning_choice_p_element.text, expected_winning_choice_p_element_text
        )
        self.assertEqual(
            winning_choice_span_element_on_breakdown.text, self.choice_1.choice_text
        )

        self.assertEqual(
            winning_choice_votes_on_breakdown_span_element.text,
            expected_winning_votes_text,
        )

    def test_all_main_voting_and_navigation_links_are_working(
        self,
    ) -> None:
        """Test all main voting and navigation links are working"""

        self.selenium.get(f"{self.live_server_url}/")

        self.pause(seconds=2)

        # First Voting
        vote_link_id = f"vote-on-poll-{self.question_1.pk}"
        vote_link = self.selenium.find_element(By.ID, vote_link_id)
        vote_link.click()

        self.pause(seconds=2)

        choice_radio_button_id = f"choice-{self.choice_2.pk}"
        choice_button = self.selenium.find_element(By.ID, choice_radio_button_id)
        choice_button.click()

        self.pause(seconds=2)

        submit_button = self.selenium.find_element(
            By.CSS_SELECTOR, 'button[type="submit"]'
        )
        submit_button.click()
        self.pause(seconds=2)

        first_update_votes_after = sum(Choice.objects.values_list("votes", flat=True))

        self.choice_2.refresh_from_db()
        choice_2_votes_after = int(self.choice_2.votes)

        self.assertGreater(choice_2_votes_after, self.choice_2_initial_votes)
        self.assertEqual(self.choice_2_initial_votes + 1, choice_2_votes_after)

        expected_votes = self.choice_2_initial_votes + self.choice_2_initial_votes + 1
        expected_text = f"{expected_votes} total responses logged"

        self.assertIn(expected_text, self.selenium.page_source)
        self.assertEqual(expected_votes, first_update_votes_after)

        winning_choice_p_element = self.selenium.find_element(
            By.ID, "winning-choice-text"
        )

        expected_winning_choice_p_element_text = self.choice_2.choice_text + " 🎉"
        winning_choice_span_element_on_breakdown = self.selenium.find_element(
            By.ID, "winning-choice-text-on-breakdown"
        )

        winning_choice_votes_on_breakdown_span_element = self.selenium.find_element(
            By.ID, "winning-choice-votes-on-breakdown"
        )

        expected_winning_votes_text = f"{self.choice_2.votes} {self.pluralize(count=self.choice_2.votes, text='vote')}"

        self.assertEqual(
            winning_choice_p_element.text, expected_winning_choice_p_element_text
        )
        self.assertEqual(
            winning_choice_span_element_on_breakdown.text, self.choice_2.choice_text
        )

        self.assertEqual(
            winning_choice_votes_on_breakdown_span_element.text,
            expected_winning_votes_text,
        )

        poll_detail_page_link = self.selenium.find_element(
            By.ID, "poll-detail-page-link"
        )

        poll_detail_page_link.click()

        self.pause(seconds=2)

        # Second Voting

        choice_radio_button_id = f"choice-{self.choice_2.pk}"
        choice_button = self.selenium.find_element(By.ID, choice_radio_button_id)
        choice_button.click()

        self.pause(seconds=2)

        submit_button = self.selenium.find_element(
            By.CSS_SELECTOR, 'button[type="submit"]'
        )
        submit_button.click()
        self.pause(seconds=2)

        second_update_votes_after = sum(Choice.objects.values_list("votes", flat=True))

        self.choice_2.refresh_from_db()
        choice_2_votes_after = int(self.choice_2.votes)

        self.assertGreater(choice_2_votes_after, self.choice_2_initial_votes + 1)
        self.assertEqual(self.choice_2_initial_votes + 1 + 1, choice_2_votes_after)

        expected_votes = (
            self.choice_2_initial_votes + self.choice_1_initial_votes + 1 + 1
        )
        expected_text = f"{expected_votes} total responses logged"

        self.assertIn(expected_text, self.selenium.page_source)
        self.assertEqual(expected_votes, second_update_votes_after)

        winning_choice_p_element = self.selenium.find_element(
            By.ID, "winning-choice-text"
        )

        expected_winning_choice_p_element_text = self.choice_2.choice_text + " 🎉"
        winning_choice_span_element_on_breakdown = self.selenium.find_element(
            By.ID, "winning-choice-text-on-breakdown"
        )

        winning_choice_votes_on_breakdown_span_element = self.selenium.find_element(
            By.ID, "winning-choice-votes-on-breakdown"
        )

        expected_winning_votes_text = f"{self.choice_2.votes} {self.pluralize(count=self.choice_2.votes, text='vote')}"

        self.assertEqual(
            winning_choice_p_element.text, expected_winning_choice_p_element_text
        )
        self.assertEqual(
            winning_choice_span_element_on_breakdown.text, self.choice_2.choice_text
        )

        self.assertEqual(
            winning_choice_votes_on_breakdown_span_element.text,
            expected_winning_votes_text,
        )

        back_to_home_link = self.selenium.find_element(By.ID, "back-to-home-link")

        back_to_home_link.click()

        header = self.selenium.find_element(By.ID, "header-app-name")
        expected_header_title = "PicklePolls"

        self.assertEqual(header.text, expected_header_title)

        self.pause(seconds=2)

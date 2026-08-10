import time
import os

import pytest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service


from utils.testing_utils.testcases import QuerySetTestMixin


@pytest.mark.django_db
class DjangoStaticLiveServerTestCase(QuerySetTestMixin, StaticLiveServerTestCase):
    """Our custom test case wrapper for tests including  StaticLiveServerTestCase."""

    maxDiff = None

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

    def pause(self, seconds: int) -> None:
        """Pause execution for amount of seconds."""
        time.sleep(seconds)

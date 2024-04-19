from django.contrib.staticfiles.testing import StaticLiveServerTestCase  # type: ignore
from utils.browser import make_chrome_browser   # type: ignore
from selenium.webdriver.common.by import By
import time


class RecipeHomePageFunctionalTest(StaticLiveServerTestCase):
    def sleep(self, seconds=5):
        time.sleep(seconds)

    def test_the_test(self):
        browser = make_chrome_browser()
        browser.get(self.live_server_url)
        self.sleep(6)
        body = browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here 🥲', body.text)
        browser.quit()

"""Functional testing of the recipe home page"""
from unittest.mock import patch

import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tests.functional_tests.recipes.base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    """Tests aimed at accessibility"""
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here 🥲', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()

        title_needed = 'This is what I need'
        recipes[0].title = title_needed
        recipes[0].save()

        # User opens the page
        self.browser.get(self.live_server_url)

        # You see a search field with the text "Search for a recipe..."
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a recipe..."]'
        )

        # Click on this 'input' and enter the search term
        # to find the title of the desired recipe.
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        # The user sees what they were looking for on the page
        self.assertIn(
            title_needed,
            self.browser.find_element(By.CLASS_NAME, 'main-content-list').text,
        )

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        self.make_recipe_in_batch()

        # User opens the page
        self.browser.get(self.live_server_url)

        # The user sees that there is pagination and clicks on page 2
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )
        page2.click()

        # The user clicks on page 2 and sees 2 more recipes
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
            2
        )

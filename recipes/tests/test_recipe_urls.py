from django.test import TestCase  # type: ignore
from django.urls import reverse  # type: ignore


class RecipeURLsTest(TestCase):
    """Testing the URLs"""

    def test_recipe_home_url_is_correct(self):
        """Test recipe home URL is correct"""
        url = reverse('recipes:home')
        self.assertEqual(url, '/')

    def test_recipe_gategory_url_is_correct(self):
        """Test recipe gategory URL is correct"""
        url = reverse('recipes:category', kwargs={'category_id': 1})
        self.assertEqual(url, '/recipes/category/1/')

    def test_recipe_detail_url_is_correct(self):
        """Test recipe detail URL is correct"""
        url = reverse('recipes:recipe', kwargs={'id': 1})
        self.assertEqual(url, '/recipes/1/')

"""Enables the creation of test classes in your Python code. These test classes
simulate the behavior of a user interacting with your application
and check whether the responses obtained are as expected."""
from django.test import TestCase  # type: ignore
from django.urls import reverse, resolve  # type: ignore
from recipes import views


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


class RecipeViewsTest(TestCase):
    '''Testing the Views'''

    def test_recipe_home_view_function_is_correct(self):
        ''' Test recipe home view function is correct'''
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_category_view_function_is_correct(self):
        ''' Test recipe category view function is correct'''
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_detail_view_function_is_correct(self):
        ''' Test recipe detail view function is correct'''
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

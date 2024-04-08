from django.test import TestCase  # type: ignore
from django.urls import reverse, resolve  # type: ignore
from recipes import views


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

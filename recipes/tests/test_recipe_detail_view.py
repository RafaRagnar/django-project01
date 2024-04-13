from django.urls import reverse, resolve  # type: ignore
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeDetailViewsTest(RecipeTestBase):
    '''Testing the Views'''

    def test_recipe_detail_view_function_is_correct(self):
        ''' Test recipe detail view function is correct'''

        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        """Test recipe detail view returns status code 404 if no recipes
        found"""

        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipes(self):
        '''Test recipe detail template loads the correct recipes'''

        needed_title = 'This is a detail page - It load one recipe'

        # Need a recipe for this test
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        content = response.content.decode('utf-8')

        # Check if one recipe exists
        self.assertIn(needed_title, content)

    def test_recipe_detail_template_dont_load_recipes_not_published(self):
        """Test recipe is_published False do not show"""

        # Need a recipe for this test
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.id}))

        self.assertEqual(response.status_code, 404)

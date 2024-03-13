from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):

    # teste de URLS
    def test_recipe_index_url_is_correct(self):
        url = reverse('recipes:index')
        self.assertEqual(url, '/')

    def test_recipe_category_url_is_correct(self):
        url = reverse(
            'recipes:category',
            kwargs={'category_id': 1}
        )
        self.assertEqual(
            url, '/recipes/category/1/'
        )

    def test_recipes_detail_url_is_correct(self):
        url = reverse(
            'recipes:recipe',
            kwargs={'pk': 1}
        )
        self.assertEqual(
            url,
            '/recipes/1'
        )

    def test_recipe_search_url_is_correct(self):
        url = reverse('recipes:search')
        self.assertEqual(
            url, '/recipes/search'
        )

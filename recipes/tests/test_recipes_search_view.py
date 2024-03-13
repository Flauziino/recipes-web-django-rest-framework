from django.urls import reverse, resolve
from recipes.views import site
from .test_recipes_base import RecipeTestBase
from unittest.mock import patch


class RecipeSearchTest(RecipeTestBase):

    def test_recipes_search_uses_correct_view_function(self):
        view = resolve(
            reverse(
                'recipes:search',
            )
        )
        self.assertIs(
            view.func.view_class, site.RecipeListSearchView
        )

    def test_recipes_search_loads_correct_template(self):
        response = self.client.get(
            reverse(
                'recipes:search',
            ) + '?q=test'
        )
        self.assertTemplateUsed(
            response, 'recipes/search.html'
        )

    def test_recipes_search_raises_404_if_no_search_termo(self):
        response = self.client.get(
            reverse(
                'recipes:search',
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?q=<Teste>'
        response = self.client.get(url)
        self.assertIn(
            'Search for &lt;Teste&gt;',
            response.content.decode('utf-8')
        )

    def test_recipe_search_can_find_recipe_by_title(self):
        title = 'This is recipe one'
        a_title = 'This is recipe two'

        recipe = self.make_recipe(
            slug='one',
            title=title,
            author_data={'username': 'one'}
        )

        a_recipe = self.make_recipe(
            slug='two',
            title=a_title,
            author_data={'username': 'two'}
        )
        response = self.client.get(
            reverse('recipes:search') + f'?q={title}'
        )
        a_response = self.client.get(
            reverse('recipes:search') + f'?q={a_title}'
        )
        response_both = self.client.get(
            reverse('recipes:search',) + '?q=This'
        )

        self.assertIn(recipe, response.context['receitas'])
        self.assertNotIn(a_recipe, response.context['receitas'])

        self.assertIn(a_recipe, a_response.context['receitas'])
        self.assertNotIn(recipe, a_response.context['receitas'])

        self.assertIn(recipe, response_both.context['receitas'])
        self.assertIn(a_recipe, response_both.context['receitas'])

    def test_recipes_search_is_paginated(self):
        self.make_recipe_in_batch(qtd=5)

        with patch('recipes.views.site.PER_PAGE', new=2):
            response = self.client.get(
                reverse('recipes:index')
            )
            recipes = response.context['receitas']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 2)
            self.assertEqual(len(paginator.get_page(2)), 2)
            self.assertEqual(len(paginator.get_page(3)), 1)

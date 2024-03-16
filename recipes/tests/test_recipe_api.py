from rest_framework import test

from django.urls import reverse

from unittest.mock import patch

from .test_recipes_base import RecipeMixin


class RecipeAPIv2Test(test.APITestCase, RecipeMixin):
    def test_recipe_api_list_returns_status_code_200(self):
        api_url = reverse(
            'recipes:recipes-api-list'
        )
        response = self.client.get(api_url)

        self.assertEqual(
            response.status_code, 200
        )

    def test_recipe_api_loads_correct_number_of_recipes(self):
        wanted_recipes = 7
        self.make_recipe_in_batch(wanted_recipes)

        api_url = reverse(
            'recipes:recipes-api-list'
        )
        response = self.client.get(api_url)

        response_count = response.data.get('count')

        self.assertEqual(
            response_count, wanted_recipes
        )

    def test_recipe_api_paginated_dafault_recipes_per_page_is_ok(self):
        wanted_recipes = 20
        self.make_recipe_in_batch(wanted_recipes)

        api_url = reverse(
            'recipes:recipes-api-list'
        )
        response = self.client.get(api_url)
        qtd_recipe_pg = len(response.data.get('results'))

        self.assertEqual(qtd_recipe_pg, 10)

    def test_recipe_api_paginated_and_number_of_pages(self):
        with patch('recipes.views.api.MyAPIv2Pagination.page_size', new=2):
            wanted_recipes = 20
            self.make_recipe_in_batch(wanted_recipes)

            api_url = reverse(
                'recipes:recipes-api-list'
            )
            response = self.client.get(api_url)

            qtd_recipe_pg = len(response.data.get('results'))
            print(response.data)

            # qtd pg1
            self.assertEqual(qtd_recipe_pg, 2)

            # testando agora se temos a 10pg e se tem 2 receitas la tb
            api_url_pg_10 = reverse(
                'recipes:recipes-api-list'
            ) + '?page10'
            response_pg_10 = self.client.get(api_url_pg_10)

            qtd_recipe_pg_10 = len(response_pg_10.data.get('results'))

            # qtd pg1
            self.assertEqual(qtd_recipe_pg_10, 2)

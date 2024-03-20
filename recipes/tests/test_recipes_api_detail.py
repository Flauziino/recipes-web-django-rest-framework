from rest_framework import test

from django.urls import reverse

from .test_recipes_base import RecipeMixin


class RecipeAPIDetailv2Test(test.APITestCase, RecipeMixin):

    def test_recipe_api_detail_returns_status_code_200(self):
        recipe = self.make_recipe()

        api_url = reverse(
            'recipes:recipes-api-detail',
            kwargs={'pk': recipe.id}
        )
        response = self.client.get(api_url)

        self.assertEqual(
            response.status_code, 200
        )

    def test_recipes_api_detail_do_not_loads_recipes_if_is_published_false(self):  # noqa: E501
        # criando a receita para o teste
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse(
                'recipes:recipes-api-detail',
                kwargs={'pk': recipe.id}
            )
        )

        # checando se o retorno é None, ja que a receita nao esta publicada
        self.assertEqual(
            response.data.get('count'), None
        )

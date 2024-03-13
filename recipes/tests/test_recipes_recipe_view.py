from django.urls import reverse, resolve
from recipes.views import site
from .test_recipes_base import RecipeTestBase


class RecipesRecipeTest(RecipeTestBase):
    # test da view recipe
    def test_recipes_recipe_views_function_is_correct(self):
        view = resolve(
            reverse(
                'recipes:recipe',
                kwargs={'pk': 1}
            )
        )
        self.assertIs(view.func.view_class, site.RecipeDetailView)

    def test_recipes_recipe_view_detail_returns_statuscode_404_(self):  # noqa: E501
        response = self.client.get(
            reverse(
                'recipes:recipe',
                kwargs={'pk': 10000}
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_recipes_recipe_template_loads_correct_recipe(self):
        # criando a receita para o teste
        needed = 'Detalhes da receita (titulo)'
        self.make_recipe(title=needed)

        response = self.client.get(
            reverse(
                'recipes:recipe',
                kwargs={'pk': 1}
            )
        )
        content = response.content.decode('utf-8')

        # checando se ela existe
        self.assertIn(needed, content)

    def test_recipes_recipe_template_do_not_loads_recipe_if_is_published_false(self):  # noqa: E501
        # criando a receita para o teste
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse(
                'recipes:recipe',
                kwargs={'pk': recipe.pk}
            )
        )

        self.assertEqual(response.status_code, 404)

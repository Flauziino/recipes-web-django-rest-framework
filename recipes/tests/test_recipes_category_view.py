from django.urls import reverse, resolve
from recipes.views import site
from .test_recipes_base import RecipeTestBase
from unittest.mock import patch


class RecipeCategoryTest(RecipeTestBase):
    # test da view category
    def test_recipes_category_views_function_is_correct(self):
        view = resolve(
            reverse(
                'recipes:category',
                kwargs={'category_id': 1}
            )
        )
        self.assertIs(view.func.view_class, site.RecipeListCategoryView)

    # teste do status code(category.view)
    def test_recipes_category_view_returns_statuscode_404_if_no_recipes(self):
        response = self.client.get(
            reverse(
                'recipes:category',
                kwargs={'category_id': 10000}
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_recipes_category_template_loads_recipes(self):
        # criando a receita para o teste
        needed = 'Categorias (titulo)'
        self.make_recipe(title=needed)

        response = self.client.get(
            reverse(
                'recipes:category',
                kwargs={'category_id': 1}
            )
        )
        content = response.content.decode('utf-8')

        # checando se ela existe
        self.assertIn(needed, content)

    def test_recipes_category_template_do_not_loads_recipes_if_is_published_false(self):  # noqa: E501
        # criando a receita para o teste
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse(
                'recipes:category',
                kwargs={'category_id': recipe.category.id}
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_recipes_category_is_paginated(self):
        self.make_recipe_in_batch(qtd=10)

        with patch('recipes.views.site.PER_PAGE', new=2):
            response = self.client.get(
                reverse('recipes:index')
            )
            recipes = response.context['receitas']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 5)
            self.assertEqual(len(paginator.get_page(1)), 2)
            self.assertEqual(len(paginator.get_page(2)), 2)
            self.assertEqual(len(paginator.get_page(3)), 2)
            self.assertEqual(len(paginator.get_page(4)), 2)
            self.assertEqual(len(paginator.get_page(5)), 2)

from django.urls import reverse, resolve
from recipes.views import site
from .test_recipes_base import RecipeTestBase
from unittest.mock import patch


class RecipeIndexTest(RecipeTestBase):

    # tests da view index
    def test_recipes_index_views_function_is_correct(self):
        view = resolve(
            reverse(
                'recipes:index'
            )
        )
        self.assertIs(view.func.view_class, site.RecipeListIndexView)

    # teste do status code(index.view)
    def test_recipes_index_view_returns_statuscode_200_OK(self):
        response = self.client.get(
            reverse(
                'recipes:index'
            )
        )

        self.assertEqual(response.status_code, 200)

    # teste do template(index.view)
    def test_recipes_index_view_loads_correct_template(self):
        response = self.client.get(
            reverse(
                'recipes:index'
            )
        )

        self.assertTemplateUsed(
            response, 'recipes/index.html'
        )

    # teste se no template renderizado pela view index tem:
    # "No momento não tem-se receitas" caso nao tenha receita na pagina
    def test_recipes_index_views_template_shows_no_momento_não_tem_se_receitas(self):  # noqa: E501
        response = self.client.get(
            reverse(
                'recipes:index'
            )
        )

        self.assertIn(
            'No momento não tem-se receitas',
            response.content.decode('utf-8'))

    def test_recipes_index_template_loads_recipes(self):
        # criando a receita para o teste
        self.make_recipe()

        response = self.client.get(
            reverse(
                'recipes:index'
            )
        )
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['receitas']

        # checando se ela existe
        self.assertIn('Recipe Title', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipes_index_template_do_not_loads_recipes_if_is_published_false(self):  # noqa: E501
        # criando a receita para o teste
        self.make_recipe(is_published=False)

        response = self.client.get(
            reverse(
                'recipes:index'
            )
        )

        # checando se ela existe
        self.assertIn(
            'No momento não tem-se receitas',
            response.content.decode('utf-8'))

    def test_recipes_index_is_paginated(self):
        self.make_recipe_in_batch(qtd=8)

        with patch('recipes.views.site.PER_PAGE', new=3):
            response = self.client.get(
                reverse('recipes:index')
            )
            recipes = response.context['receitas']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 2)

    def test_pagination_current_page_conversion_with_invalid_value_again_but_with_dif_type_of_test(self):  # noqa: E501
        # testando o pagination para pagina "invalida" em outro local
        # para ver se levanta o "valueerror" e o "current_page" se torna 1
        self.make_recipe_in_batch(qtd=8)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(
                reverse('recipes:index') + '?page=invalid'
            )

            self.assertEqual(
                response.context['receitas'].number,
                1
            )

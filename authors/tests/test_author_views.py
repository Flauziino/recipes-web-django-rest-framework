from django.forms import ValidationError
from authors.forms.recipe_form import AuthorRecipeForm
from authors.views import DashboardRecipeEdit

from recipes.models import Recipe

from recipes.tests.test_recipes_base import RecipeMixin

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from unittest.mock import patch


class AuthorClassViewTest(TestCase, RecipeMixin):

    def setUp(self, *args, **kwargs):

        self.user = User.objects.create_user(
            username='my_user',
            password='my_pass'
        )
        self.client.force_login(
            self.user
        )

        self.recipe = Recipe.objects.create(
            category=self.make_category(),
            author=self.user,
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
            preparation_steps_is_html=False,
            is_published=False,
        )

        self.form_data = {
            'title': self.recipe.title,
            'description': self.recipe.description,
            'preparation_time': self.recipe.preparation_time,
            'preparation_time_unit': self.recipe.preparation_time_unit,
            'servings': self.recipe.servings,
            'servings_unit': self.recipe.servings_unit,
            'preparation_steps': self.recipe.preparation_steps,
        }

        return super().setUp(*args, **kwargs)

    def test_dashboard_recipe_edit_method_get_recipe_got_recipe(self):
        response = self.client.get(
            reverse(
                'authors:dashboard_edit',
                kwargs={'id': self.recipe.id}
            )
        )

        content = response.content.decode('utf-8')
        self.assertIn('Recipe Title', content)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_recipe_edit_method_get_recipe_didnt_get_recipe(self):
        fake_id = self.recipe.id + 1
        response = self.client.get(
            reverse(
                'authors:dashboard_edit',
                kwargs={'id': fake_id}
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_dashboard_recipe_edit_method_post_get_recipe(self):
        view = DashboardRecipeEdit()
        response = self.client.post(
            reverse(
                'authors:dashboard_edit',
                kwargs={'id': self.recipe.id}
            ),

        )
        view.request = response
        response.user = self.user
        receita = view.get_recipe(self.recipe.id)

        self.assertEqual(receita, self.recipe)

    def test_dashboard_recipe_edit_method_post_with_complete_valid_form(self):
        new_title = 'Receita Att'
        self.form_data['title'] = new_title

        response = self.client.post(
            reverse(
                'authors:dashboard_edit',
                kwargs={'id': self.recipe.id}
            ),
            data=self.form_data,
            follow=True
        )

        # verificando se redirecionou
        self.assertEqual(response.status_code, 200)
        # verificando a msg de sucesso
        self.assertContains(response, 'Sua receita foi salva com sucesso!')

        # pegando ultima receita
        last_one = Recipe.objects.latest('id')
        # testando se ta correto
        self.assertEqual(last_one.title, new_title)

    def test_dashboard_recipe_create_method_get(self):

        response = self.client.get(
            reverse(
                'authors:dashboard_create',
            ),
        )

        context = response.context['form']
        self.assertIn(
            'Dashboard nova receita',
            response.content.decode('utf-8')
        )
        self.assertIsInstance(
            context, AuthorRecipeForm
        )

    def test_dashboard_recipe_create_method_post_create_a_new_recipe_valid_form(self):  # noqa : E501
        new_title = 'Nova Receita'
        new_description = 'Descript Teste'
        self.form_data['title'] = new_title
        self.form_data['description'] = new_description

        response = self.client.post(
            reverse(
                'authors:dashboard_create',
            ),
            data=self.form_data,
            follow=True
        )
        # verificando se redirecionou
        self.assertEqual(response.status_code, 200)
        # verificando a msg de sucesso
        self.assertContains(
            response,
            'Sua receita foi salva com sucesso!'
        )
        # pegando ultima receita
        new_one = Recipe.objects.latest('id')
        # testando se ta correto
        self.assertEqual(new_one.title, new_title)
        self.assertEqual(new_one.description, new_description)

    def test_dashboard_recipe_create_method_post_recipe_invalid_form(self):
        invalid_title = ''
        self.form_data['title'] = invalid_title
        # simulando o clean da validaçao do form falhando
        with patch.object(AuthorRecipeForm, 'clean') as mock_clean:
            mock_clean.side_effect = ValidationError(
                'O título deve ter pelo menos 5 caracteres'
            )
            response = self.client.post(
                reverse('authors:dashboard_create'),
                data=self.form_data
            )
            # verificando se ainda renderizou
            self.assertEqual(response.status_code, 200)
            # verificando que o form é invalido
            form = response.context['form']
            self.assertFalse(form.is_valid())
            # verificando se a msg de erro ao criar receita apareceu
            self.assertContains(
                response, 'Existem erros em seu formulário!'
            )

    def test_dashboard_recipe_delite_post_method_delete_a_recipe(self):

        # primeiro cria receita
        new_title = 'Nova Receita'
        new_description = 'Descript Teste'
        self.form_data['title'] = new_title
        self.form_data['description'] = new_description

        response = self.client.post(
            reverse(
                'authors:dashboard_create',
            ),
            data=self.form_data,
            follow=True
        )

        self.assertContains(
            response,
            'Sua receita foi salva com sucesso!'
        )

        # Enviar uma solicitação POST para excluir
        # a receita criada anteriormente
        del_response = self.client.post(
            reverse(
                'authors:dashboard_delete'
            ),
            data={'id': self.recipe.id},
            follow=True
        )
        # Verificar que a resposta redireciona para a página de dashboard
        self.assertRedirects(
            del_response, reverse('authors:dashboard')
        )
        # Captando a msg de sucesso quando a receita é deletada
        self.assertContains(
            del_response, 'Receita apagada com sucesso!'
        )
        # Verificar que a receita foi excluída do banco de dados
        with self.assertRaises(Recipe.DoesNotExist):
            Recipe.objects.get(pk=self.recipe.id)

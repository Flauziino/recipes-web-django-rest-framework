from django.forms import ValidationError

from .test_author_views import AuthorClassViewTest

from django.urls import reverse


class AuthorRecipeFormTest(AuthorClassViewTest):

    def test_validations_raise_errors_authors_recipe_form(self):
        # criando um formulario invalido
        new_title = 'aaa'
        new_description = 'aaa'
        new_preparation_time = -1
        new_servings = -1
        self.form_data['title'] = new_title
        self.form_data['description'] = new_description
        self.form_data['preparation_time'] = new_preparation_time
        self.form_data['servings'] = new_servings

        response = self.client.post(
            reverse(
                'authors:dashboard_create',
            ),
            data=self.form_data,
        )

        self.assertRaises(ValidationError)
        self.assertContains(
            response, 'Existem erros em seu formulário!'
        )
        self.assertContains(
            response, 'O título deve ter pelo menos 5 caracteres'
        )
        self.assertContains(
            response, 'O tempo de preparo não pode ser negativo'
        )
        self.assertContains(
            response, 'As porções não podem ter valor negativo'
        )

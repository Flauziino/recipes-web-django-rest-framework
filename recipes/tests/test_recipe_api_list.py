from rest_framework import test

from django.urls import reverse

from unittest.mock import patch

from .test_recipes_base import RecipeMixin


class RecipeAPIv2Test(test.APITestCase, RecipeMixin):

    def get_auth_data(self, username='user', password='password'):
        userdata = {
            'username': username,
            'password': password
        }
        user = self.make_author(
            username=userdata.get('username'),
            password=userdata.get('password')
        )
        response = self.client.post(
            reverse('recipes:token_obtain_pair'), data={**userdata}
        )
        return {
            'jwt_access_token': response.data.get('access'),
            'jwt_refresh_token': response.data.get('refresh'),
            'user': user,
        }

    def get_recipe_raw_data(self):
        return {
            'title': 'Title',
            'description': 'Description',
            'preparation_time': 1,
            'preparation_time_unit': 'Hora',
            'servings': 1,
            'servings_unit': 'Pessoa',
            'preparation_steps': 'step by step'
        }

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

    def test_recipes_api_do_not_loads_recipes_if_is_published_false(self):  # noqa: E501
        # criando a receita para o teste
        self.make_recipe(is_published=False)

        response = self.client.get(
            reverse(
                'recipes:recipes-api-list'
            )
        )

        # checando se ela existe
        self.assertEqual(
            response.data.get('count'), 0
        )

    def test_recipe_api_list_loads_recipes_by_category_id(self):
        # criando duas categorias (desejada e nao desejada)
        category_wanted = self.make_category(name='WANTED CATEGORY')
        category_not_wanted = self.make_category(name='NOT_WANTED CATEGORY')

        # criando 10 receitas
        recipes = self.make_recipe_in_batch(qtd=10)

        # fazendo todas receitas ter a categoria desejada
        for recipe in recipes:
            recipe.category = category_wanted
            recipe.save()

        # mudando a categoria de apenas uma receita para a nao desejada
        recipes[0].category = category_not_wanted
        recipes[0].save()

        api_url = reverse(
            'recipes:recipes-api-list'
        ) + f'?category_id={category_wanted.id}'
        response = self.client.get(api_url)

        # checando se tem a quantidade desejada
        # das categorias que estamos buscando
        self.assertEqual(
            response.data.get('count'), 9
        )

        # conferindo se o mesmo ocorre para a outra categoria
        api_url = reverse(
            'recipes:recipes-api-list'
        ) + f'?category_id={category_not_wanted.id}'
        response = self.client.get(api_url)
        self.assertEqual(
            response.data.get('count'), 1
        )

    def test_recipe_api_list_user_must_send_jwt_token_to_create_recipe(self):
        api_url = reverse(
            'recipes:recipes-api-list'
        )
        response = self.client.post(api_url)
        self.assertEqual(
            response.status_code, 401
        )

    def test_recipe_api_list_logged_user_can_create_a_recipe(self):
        # faz a receita
        recipe_raw_data = self.get_recipe_raw_data()
        auth_data = self.get_auth_data()
        jwt_access = auth_data.get('jwt_access_token')

        # url
        api_url = reverse(
            'recipes:recipes-api-list'
        )

        # realiza o post para usuario logado
        response = self.client.post(
            api_url,
            data=recipe_raw_data,
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'
        )

        # checa se foi criada a receita (codigo 201)
        self.assertEqual(
            response.status_code, 201
        )

    def test_recipe_api_list_logged_user_can_update_a_recipe(self):
        # Config do teste
        recipe = self.make_recipe()
        access_data = self.get_auth_data()
        jwt_access = access_data.get('jwt_access_token')
        author = access_data.get('user')
        recipe.author = author
        recipe.save()
        # url
        api_url = reverse(
            'recipes:recipes-api-detail', args=(recipe.id,)
        )

        # realiza o patch com o usuario correto logado
        response = self.client.patch(
            api_url,
            data={
                'title': f'Title update by {author}'
            },
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'
        )

        # checando se foi atualizada com novo titulo utilizando "CONTAINS"
        self.assertContains(
            response,
            f'Title update by {author}'
        )

    def test_recipe_api_list_logged_user_can_only_update_your_own_recipe(self):
        # Config do teste
        recipe = self.make_recipe()

        # Usuario que pode atualizar (dono)
        access_data = self.get_auth_data(username='can_update')

        # Pegando o access para usuario que NAO pode atualizar
        another_user = self.get_auth_data(username='cant_update')
        jwt_access = another_user.get('jwt_access_token')

        # Linkando o usuario que PODE atualizar a receita (dono)
        author = access_data.get('user')
        recipe.author = author
        recipe.save()

        # url
        api_url = reverse(
            'recipes:recipes-api-detail', args=(recipe.id,)
        )

        # tenta realizar o patch (update)
        # com o usuario que NAO é dono da receita
        response = self.client.patch(
            api_url,
            data={},
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'
        )

        # checando se o codigo foi "forbiden" (403), pois usuario n tem acesso
        # pois nao é o dono dessa receita
        self.assertEqual(
            response.status_code, 403
        )

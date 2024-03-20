from django.urls import reverse

from rest_framework import serializers

from .test_recipes_api_list import RecipeAPIListv2Test

from recipes.serializers import RecipeSerializer


class RecipeAPIListv2Test(RecipeAPIListv2Test):

    def test_recipes_serializer_validations_raise_errors(self):
        # faz a receita valida
        recipe_raw_data = self.get_recipe_raw_data()

        # dados de acesso do usuario, pois só pode criar a receita estando
        # logado
        auth_data = self.get_auth_data()
        jwt_access = auth_data.get('jwt_access_token')

        # invalidando os dados da receita para levantar os erros
        new_title = 'aaa'
        new_description = 'aaa'
        new_preparation_time = -1
        new_servings = -1

        recipe_raw_data['title'] = new_title
        recipe_raw_data['description'] = new_description
        recipe_raw_data['preparation_time'] = new_preparation_time
        recipe_raw_data['servings'] = new_servings

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

        # checa inicialmente se recebeu um bad request (code 400)
        self.assertEqual(
            response.status_code, 400
        )
        # checa se deu raise no error do serializer
        self.assertRaises(serializers.ValidationError)

        # checa se todas as msg de erros estao contidas no serializer
        self.assertContains(
            response,
            "O título deve ter pelo menos 5 caracteres",
            status_code=400
        )

        self.assertContains(
            response,
            "O título não pode ser igual a descrição",
            status_code=400
        )

        self.assertContains(
            response,
            "A descrição não pode ser igual ao título",
            status_code=400
        )

        self.assertContains(
            response,
            "O tempo de preparo não pode ser negativo",
            status_code=400
        )

        self.assertContains(
            response,
            "As porções não podem ter valor negativo",
            status_code=400
        )

    def test_recipes_serializer_positive_number_method_return_none_if_erros(self):  # noqa : E501
        # instanciando para poder chamar o metodo
        serializer = RecipeSerializer()
        # chamando um metodo passando uma string que nao pode ser convertida p
        # um numero inteiro
        serializer = serializer.is_number('abc')

        self.assertEqual(serializer, None)
        # ou
        self.assertIsNone(serializer)

    def test_recipes_serializer_can_convert_a_string_to_number(self):
        # instanciando para poder chamar o metodo
        serializer = RecipeSerializer()
        # chamando um metodo passando uma string que pode ser convertida p
        # um numero inteiro
        serializer = serializer.is_number('1')
        self.assertEqual(serializer, 1)

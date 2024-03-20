from django.urls import reverse

from recipes.tests.test_recipes_api_list import RecipeAPIListv2Test


class AuthorAPIListv2Test(RecipeAPIListv2Test):

    def test_author_api_list_returns_status_code_401_if_not_logged(self):
        api_url = reverse(
            'authors:author-api-list'
        )
        response = self.client.get(api_url)

        self.assertEqual(
            response.status_code, 401
        )

    def test_author_api_list_returns_status_code_200_if_logged(self):
        access_data = self.get_auth_data()
        jwt_access = access_data.get('jwt_access_token')

        api_url = reverse(
            'authors:author-api-list'
        )
        response = self.client.get(
            api_url,
            data={},
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'
        )

        self.assertEqual(
            response.status_code, 200
        )

    def test_author_api_list_queryset_return_right_user_username(self):
        access_data = self.get_auth_data()
        jwt_access = access_data.get('jwt_access_token')

        api_url = reverse(
            'authors:author-api-list'
        )

        self.client.get(
            api_url,
            data={},
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'
        )
        user = access_data.get('user')

        self.assertEqual(
            user.username, 'user'
        )

    def test_author_api_ME_returns_status_code_401_if_not_logged(self):
        api_url = reverse(
            'authors:author-api-me'
        )
        response = self.client.get(api_url)

        self.assertEqual(
            response.status_code, 401
        )

    def test_author_api_ME_returns_status_code_200_if_logged(self):
        access_data = self.get_auth_data()
        jwt_access = access_data.get('jwt_access_token')

        api_url = reverse(
            'authors:author-api-me'
        )
        response = self.client.get(
            api_url,
            data={},
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'
        )

        self.assertEqual(
            response.status_code, 200
        )

    def test_author_api_ME_queryset_return_right_user_username(self):
        access_data = self.get_auth_data()
        jwt_access = access_data.get('jwt_access_token')

        api_url = reverse(
            'authors:author-api-me'
        )

        self.client.get(
            api_url,
            data={},
            HTTP_AUTHORIZATION=f'Bearer {jwt_access}'
        )
        user = access_data.get('user')

        self.assertEqual(
            user.username, 'user'
        )

from django.test import TestCase
from django.contrib.auth.models import User

from authors.models import Profile


class AuthorsProfileTest(TestCase):
    def test_profile_model_method_str_returns_the_right_value(self):
        # cria autor
        author = User.objects.create(
            first_name='first',
            last_name='last',
            username='user_test'
        )
        # pegar o perfil do autor que foi criado automaticamente ao criar
        # o autor
        perfil = Profile.objects.get(author=author)

        self.assertEqual(
            str(perfil), author.username
        )

from unittest import TestCase

from django.contrib.auth.models import User
from django.test import TestCase as DjangoTestCase
from django.urls import reverse

from authors.forms import RegisterForm

from parameterized import parameterized


class AuthorRegisterFormTest(TestCase):
    def test_first_name_placeholder_is_correct(self):
        form = RegisterForm()
        placeholder = form['first_name'].field.widget.attrs['placeholder']
        self.assertEqual(
            'Ex.: John', placeholder
        )

    def test_last_name_placeholder_is_correct(self):
        form = RegisterForm()
        placeholder = form['last_name'].field.widget.attrs['placeholder']
        self.assertEqual(
            'Ex.: Doe', placeholder
        )

    def test_email_placeholder_is_correct(self):
        form = RegisterForm()
        placeholder = form['email'].field.widget.attrs['placeholder']
        self.assertEqual(
            'Ex: John@email.com', placeholder
        )

    def test_username_placeholder_is_correct(self):
        form = RegisterForm()
        placeholder = form['username'].field.widget.attrs['placeholder']
        self.assertEqual(
            'Seu nome de usuário', placeholder
        )

    def test_password_placeholder_is_correct(self):
        form = RegisterForm()
        placeholder = form['password'].field.widget.attrs['placeholder']
        self.assertEqual(
            'Sua senha', placeholder
        )

    def test_password2_placeholder_is_correct(self):
        form = RegisterForm()
        placeholder = form['password2'].field.widget.attrs['placeholder']
        self.assertEqual(
            'Confirme sua senha', placeholder
        )

    @parameterized.expand([
        ('password', (
            'A senha deve conter pelo menos uma letra maiúscula, '
            'uma letra minúscula e um número. O comprimento deve ser '
            'pelo menos 8 caracteres.'
            )
         ),
        ('username', (
            'O campo deve ter letras, números e @.+-_ apenas.'
            'Deve estar entre 4 e 150 caracteres.'
            )
         ),
        ('email', 'Digite um e-mail válido')
    ])
    def test_field_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)

    @parameterized.expand([
        ('first_name', 'Nome'),
        ('last_name', 'Sobrenome'),
        ('username', 'Usuário'),
        ('email', 'E-mail'),
        ('password', 'Senha'),
        ('password2', 'Confirme sua senha'),
    ])
    def test_fields_labels(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, needed)


class AuthorRegisterIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'firstname',
            'last_name': 'lastname',
            'email': 'emailuser@email.com',
            'password': 'Str0123456b',
            'password2': 'Str0123456b',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'Este campo é obrigatório'),
        ('first_name', 'Escreve seu nome'),
        ('last_name', 'Escreve seu sobrenome'),
        ('email', 'O campo e-mail não pode ficar em branco'),
        ('password', 'O campo não pode estar vazio'),
        ('password2', 'Este campo é obrigatório.'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ' '
        url = reverse('authors:create')
        response = self.client.post(
            url, data=self.form_data, follow=True
        )
        self.assertIn(
            msg, response.content.decode('utf-8')
        )

    def test_username_field_min_length_shoud_be_4_char(self):
        # testanto a msg de erro de min_length
        self.form_data['username'] = 'joa'
        url = reverse('authors:create')
        response = self.client.post(
            url, data=self.form_data, follow=True
        )
        msg = 'Deve conter pelo menos 4 caracteres'
        self.assertIn(
            msg, response.content.decode('utf-8')
        )

    def test_username_field_max_length_shoud_be_less_than_150_char(self):
        # testando a msg de erro de max_length
        self.form_data['username'] = ('j' * 151)
        url = reverse('authors:create')
        response = self.client.post(
            url, data=self.form_data, follow=True
        )
        msg = 'Deve ter no máximo 150 caracteres'
        self.assertIn(
            msg, response.content.decode('utf-8')
        )

    def test_password_field_has_upper_lower_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'
        url = reverse('authors:create')
        response = self.client.post(
            url, data=self.form_data, follow=True
        )
        msg = (
            'A senha deve conter pelo menos uma letra maiúscula,'
            ' uma letra minúscula e um número.'
            ' O comprimento deve ser pelo menos 8 caracteres.'
            )

        self.assertIn(
            msg, response.content.decode('utf-8')
        )

    def test_password_and_password2_are_equal_and_strong(self):
        self.form_data['password'] = 'Abc123456'
        self.form_data['password2'] = 'Abc123456'

        url = reverse('authors:create')
        response = self.client.post(
            url, data=self.form_data, follow=True
        )
        msg = 'As duas senhas precisam ser iguais!'

        self.assertNotIn(
            msg, response.content.decode('utf-8')
        )

    def test_password_and_password_2_must_be_equal(self):
        self.form_data['password'] = 'Abc123456'
        self.form_data['password2'] = 'Abc1234567'
        url = reverse('authors:create')
        response = self.client.post(
            url, data=self.form_data, follow=True
        )
        msg = 'As duas senhas precisam ser iguais!'
        self.assertIn(
            msg, response.content.decode('utf-8')
        )

    def test_send_get_request_to_registration_create_views_return_404(self):
        url = reverse('authors:create')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code, 404
        )

    def test_authors_register_view_loads_correct_template(self):
        response = self.client.get(
            reverse(
                'authors:register'
            )
        )

        self.assertTemplateUsed(
            response, 'author/register_view.html'
            )

    def test_authors_register_view_context(self):
        response = self.client.get(
            reverse(
                'authors:register'
            )
        )

        self.assertTemplateUsed(
            response, 'author/register_view.html'
            )

        content = response.content.decode('utf-8')

        # checando se ela existe
        self.assertIn('form', content)

    def test_email_must_be_unique(self):
        url = reverse('authors:create')

        self.client.post(
            url, data=self.form_data, follow=True
            )

        response = self.client.post(
            url, data=self.form_data, follow=True
        )

        msg = 'O e-mail ja esta cadastrado na base de dados!'

        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_author_created_can_login(self):
        url = reverse('authors:create')

        self.form_data.update({
            'username': 'testuser',
            'password': 'A@bc123456',
            'password2': 'A@bc123456',
        })

        self.client.post(
            url, data=self.form_data, follow=True
            )

        is_authenticated = self.client.login(
            username='testuser',
            password='A@bc123456'
        )

        self.assertTrue(is_authenticated)


class AuthorLogoutTest(DjangoTestCase):
    def test_user_tries_to_logout_using_get_method(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')

        response = self.client.get(
            reverse('authors:logout'),
            follow=True
        )

        self.assertIn(
            'Você precisa estar logado para realizar esta ação',
            response.content.decode('utf-8')
        )

    def test_user_tries_to_logout_using_another_user(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')

        response = self.client.post(
            reverse('authors:logout'),
            data={
                'username': 'another_user'
            },
            follow=True
        )

        self.assertIn(
            'Este usuário não tem acesso a esta página',
            response.content.decode('utf-8')
        )

    def test_user_can_logout_successfully(self):
        User.objects.create_user(username='my_user', password='my_pass')
        self.client.login(username='my_user', password='my_pass')

        response = self.client.post(
            reverse('authors:logout'),
            data={
                'username': 'my_user'
            },
            follow=True
        )

        self.assertIn(
            'Deslogado com sucesso!',
            response.content.decode('utf-8')
        )

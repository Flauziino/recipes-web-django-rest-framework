from .base import AuthorsBaseTest

from selenium.webdriver.common.by import By

from django.contrib.auth.models import User
from django.urls import reverse


class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        string_password = 'Abc@123456'
        user = User.objects.create_user(
            username='my_user',
            password=string_password
        )

        # Usuario abre a pg de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Usuário ve o formulario de login
        form = self.get_form_1()

        username_field = self.get_by_placeholder(
            form, 'Escreva seu usuário aqui'
        )

        password_field = self.get_by_placeholder(
            form, 'Escreva sua senha aqui'
        )

        # Usuário digita seu usuário e senha
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        # Usuário envia o form
        form.submit()

        self.assertIn(
            'Logado com sucesso!',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_user_cant_login_error_message_incorrect_user_or_password(self):
        string_password = 'Abc@123456'
        user = User.objects.create_user(
            username='my_user',
            password=string_password
        )

        # Usuario abre a pg de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Usuário ve o formulario de login
        form = self.get_form_1()

        username_field = self.get_by_placeholder(
            form, 'Escreva seu usuário aqui'
        )

        password_field = self.get_by_placeholder(
            form, 'Escreva sua senha aqui'
        )

        # Usuário digita seu usuário e senha
        username_field.send_keys(user.username)
        password_field.send_keys('Abc@12345')

        # Usuário envia o form
        form.submit()

        self.assertIn(
            'Falha ao logar, usuário ou senha inválidos',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_user_cant_login_error_message_invalid_form(self):
        string_password = ' '
        user = User.objects.create_user(
            username=' ',
            password=string_password
        )

        # Usuario abre a pg de login
        self.browser.get(self.live_server_url + reverse('authors:login'))

        # Usuário ve o formulario de login
        form = self.get_form_1()

        username_field = self.get_by_placeholder(
            form, 'Escreva seu usuário aqui'
        )

        password_field = self.get_by_placeholder(
            form, 'Escreva sua senha aqui'
        )

        # Usuário digita seu usuário e senha
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        # Usuário envia o form
        form.submit()

        self.assertIn(
            'Falha ao logar, usuário ou senha inválidos',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(
            self.live_server_url +
            reverse('authors:login_create')
        )

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

from .base import AuthorsBaseTest
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By


class AuthorsRegisterTest(AuthorsBaseTest):

    def test_empty_first_name_error_message(self):
        def callback(form):

            first_name_field = self.get_by_placeholder(form, 'Ex.: John')
            first_name_field.send_keys(' ')
            first_name_field.send_keys(Keys.ENTER)

            form = self.get_form_2()

            self.assertIn(
                'Escreve seu nome', form.text
            )

        self.form_field_test_with_callback(callback)

    def test_empty_last_name_error_message(self):
        def callback(form):

            last_name_field = self.get_by_placeholder(form, 'Ex.: Doe')
            last_name_field.send_keys(' ')
            last_name_field.send_keys(Keys.ENTER)

            form = self.get_form_2()

            self.assertIn(
                'Escreve seu sobrenome', form.text
            )

        self.form_field_test_with_callback(callback)

    def test_empty_username_error_message(self):
        def callback(form):

            username_field = self.get_by_placeholder(
                form, 'Seu nome de usuário'
            )
            username_field.send_keys(' ')
            username_field.send_keys(Keys.ENTER)

            form = self.get_form_2()

            self.assertIn(
                'Este campo é obrigatório', form.text
            )

        self.form_field_test_with_callback(callback)

    def test_invalid_email_error_message(self):
        def callback(form):

            email_field = self.get_by_placeholder(
                form, 'Ex: John@email.com'
            )
            email_field.send_keys('email@invalid')
            email_field.send_keys(Keys.ENTER)

            form = self.get_form_1()

            self.assertIn(
                'Digite um e-mail válido', form.text
            )

        self.form_field_test_with_callback(callback)

    def test_empty_password_error_message(self):
        def callback(form):

            password_field = self.get_by_placeholder(
                form, 'Sua senha'
            )
            password_field.send_keys(' ')
            password_field.send_keys(Keys.ENTER)

            form = self.get_form_2()

            self.assertIn(
                'O campo não pode estar vazio', form.text
            )

        self.form_field_test_with_callback(callback)

    def test_password1_and_password2_must_be_equal(self):
        def callback(form):

            password1_field = self.get_by_placeholder(
                form, 'Sua senha'
            )
            password2_field = self.get_by_placeholder(
                form, 'Confirme sua senha'
            )
            password1_field.send_keys('Abc@12345')
            password2_field.send_keys('Abc@123456')
            password2_field.send_keys(Keys.ENTER)

            form = self.get_form_2()

            self.assertIn(
                'As duas senhas precisam ser iguais!', form.text
            )

        self.form_field_test_with_callback(callback)

    def test_user_valid_data_register_successfully(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form_1()

        self.get_by_placeholder(form, 'Ex.: John').send_keys('Nometest')
        self.get_by_placeholder(form, 'Ex.: Doe').send_keys('Sobrenome')

        self.get_by_placeholder(
            form, 'Seu nome de usuário'
        ).send_keys('testuser')

        self.get_by_placeholder(
            form, 'Ex: John@email.com'
        ).send_keys('emailtest@email.com')

        self.get_by_placeholder(form, 'Sua senha').send_keys('Abc@12345')
        self.get_by_placeholder(
            form, 'Confirme sua senha'
        ).send_keys('Abc@12345')

        form.submit()

        self.assertIn(
            'Cadastro realizado com sucesso!',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

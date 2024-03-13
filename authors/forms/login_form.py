from django import forms
from utils.placeholder import add_placeholder


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Escreva seu usuário aqui')
        add_placeholder(self.fields['password'], 'Escreva sua senha aqui')

    username = forms.CharField(
        label='Usuário',
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput()
    )

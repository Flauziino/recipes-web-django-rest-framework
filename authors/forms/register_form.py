from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from utils.placeholder import add_placeholder
from utils.strong_password import strong_password


class RegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username',
            'email', 'password'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Seu nome de usuário')
        add_placeholder(self.fields['email'], 'Ex: John@email.com')
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')

    first_name = forms.CharField(
        error_messages={'required': 'Escreve seu nome'},
        label='Nome'
    )

    last_name = forms.CharField(
        error_messages={'required': 'Escreve seu sobrenome'},
        label='Sobrenome'
    )

    username = forms.CharField(
        label='Usuário',
        help_text=(
            'O campo deve ter letras, números e @.+-_ apenas.'
            'Deve estar entre 4 e 150 caracteres.'
        ),
        error_messages={
            'required': 'Este campo é obrigatório',
            'min_length': 'Deve conter pelo menos 4 caracteres',
            'max_length': 'Deve ter no máximo 150 caracteres',
        },
        min_length=4,
        max_length=150,
    )

    email = forms.EmailField(
        error_messages={'required': 'O campo e-mail não pode ficar em branco'},
        label='E-mail',
        help_text='Digite um e-mail válido'
    )

    password = forms.CharField(
        label='Senha',
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Sua senha'
        }),
        error_messages={
            'required': 'O campo não pode estar vazio'
        },
        help_text=(
            'A senha deve conter pelo menos uma letra maiúscula, '
            'uma letra minúscula e um número. O comprimento deve ser '
            'pelo menos 8 caracteres.'
        ),
        validators=[strong_password]
    )
    password2 = forms.CharField(
        label='Confirme sua senha',
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirme sua senha'
        })
    )

    # Apenas um exemplo de validação de campo para ficar salvo
    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'O e-mail ja esta cadastrado na base de dados!'
            )

        return email

    # validaçao generalista
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise ValidationError(
                {
                    'password': 'As duas senhas precisam ser iguais!',
                    'password2': 'As duas senhas precisam ser iguais!'
                }
            )

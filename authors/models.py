from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    author = models.OneToOneField(
        User,
        verbose_name='Autor',
        on_delete=models.CASCADE
    )
    bio = models.TextField(
        verbose_name='Biografia',
        default='',
        blank=True
    )

    def __str__(self):
        return self.author.username

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from tag.models import Tag

from utils.imagem import resize_image
from utils.slug import new_slug


class Category(models.Model):

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    name = models.CharField(
        max_length=65
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):

    class Meta:
        verbose_name = 'Receita'
        verbose_name_plural = 'Receitas'

    title = models.CharField(
        verbose_name='Título',
        max_length=65,
    )

    description = models.CharField(
        verbose_name='Descrição',
        max_length=255,
    )

    slug = models.SlugField(
        unique=True,
        default=None,
        null=True,
        blank=True,
        max_length=95
    )

    preparation_time = models.IntegerField(
        verbose_name='Tempo de preparação'
    )

    preparation_time_unit = models.CharField(
        verbose_name='Tempo de preparação unitário',
        max_length=65,
    )

    servings = models.IntegerField(
        verbose_name='Porções'
    )

    servings_unit = models.CharField(
        max_length=65,
        verbose_name='Tipo da porção'
    )

    preparation_steps = models.TextField(
        verbose_name='Passo a passo da preparação'
    )

    preparation_steps_is_html = models.BooleanField(
        default=False,
        verbose_name='O passo a passo é HTML?'
    )

    created_at = models.DateTimeField(
        verbose_name='Criado em',
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        verbose_name='Atualizado em',
        auto_now=True
    )

    is_published = models.BooleanField(
        default=False,
        verbose_name='Está publicado?'
    )

    cover = models.ImageField(
        upload_to='recipes/cover/%Y/%m/%d/',
        verbose_name='Imagem da receita',
        blank=True,
        default='',
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        default=None,
        verbose_name='Categoria'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Autor'
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        default=''
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'recipes:recipe', kwargs={'pk': self.id}
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = new_slug(self.title)

        current_cover_name = str(self.cover.name)
        super_save = super().save(*args, **kwargs)
        cover_changed = False

        if self.cover:
            cover_changed = current_cover_name != self.cover.name

        if cover_changed:
            resize_image(self.cover, 468, 360, True, 70)

        return super_save

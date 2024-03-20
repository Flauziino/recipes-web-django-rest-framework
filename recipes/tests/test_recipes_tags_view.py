from django.urls import reverse, resolve

from recipes import views

from .test_recipes_base import RecipeTestBase

from tag.models import Tag


class RecipesTagsTest(RecipeTestBase):

    def setUp(self):
        self.tag = Tag.objects.create(
            name='uma tag',
            slug='uma-tag'
        )

    def make_tag_in_batch(self, qtd=10):
        tags = []
        for i in range(qtd):
            kwargs = {
                'name': f'Tag Title {i}',
                'slug': f'tag-title-{i}',
            }
            tag = Tag.objects.create(**kwargs)
            tags.append(tag)

        return tags

    def test_recipes_tag_views_function_is_correct(self):
        view = resolve(
            reverse(
                'recipes:tag',
                kwargs={'slug': self.tag.slug}
            )
        )
        self.assertIs(view.func.view_class, views.RecipeListTagView)

    def test_recipes_tag_view_returns_Tag_nao_encontrada_if_no_tags(self):
        response = self.client.get(
            reverse(
                'recipes:tag',
                kwargs={'slug': 'd1221d1d12d2'}
            )
        )

        self.assertContains(
            response,
            'Tag não encontrada!'
        )

    def test_recipes_tag_template_loads_tags(self):
        response = self.client.get(
            reverse(
                'recipes:tag',
                kwargs={'slug': self.tag.slug}
            )
        )
        self.assertContains(
            response,
            self.tag.name
        )

    # como o APP tag esta sendo utilizado SOMENTE dentro do app RECIPES
    # o test do model TAG sera feito aqui mesmo.
    def test_tag_model_create_slug_automatic(self):
        tag = Tag.objects.create(
            name='Uma linda tag'
        )

        # foi feito fatiamento, pois na funcao de criaçao de slug,
        # ainda tem digitos completamente randomicos no fim
        # por conta disso fatiou-se para ignorar esses chars e verificar
        # se o titulo da tag esta dentro da slug
        self.assertEqual(
            tag.slug[:13], 'uma-linda-tag'
        )

        # é possivel utilizar dessa forma tb.
        self.assertIn(
            'uma-linda-tag', tag.slug
        )

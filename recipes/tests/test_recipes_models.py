import io

from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError

from parameterized import parameterized

from .test_recipes_base import RecipeTestBase, Recipe


class RecipeModelsTest(RecipeTestBase):

    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_defaults(self):
        recipe = Recipe(
            category=self.make_category(name='Test Default Category'),
            author=self.make_author(username='newuser'),
            title='Recipe Title No Defaults',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand([
        ('title', 65),
        ('description', 255),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(
            self.recipe, field,
            'A' * (max_length + 5)
        )
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(
            recipe.preparation_steps_is_html,
            msg='Recipe preparation_steps_is_html is not False',
        )

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(
            recipe.is_published,
            msg='Recipe is_published is not False',
        )

    def test_recipe_string_representation(self):
        self.recipe.title = 'Testing representation'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(
            str(self.recipe), 'Testing representation'
        )

    # Model category
    def test_category_name_raises_error_if_title_has_more_than_65_chars(self):
        category = self.make_category(name="Testing")
        category.name = 'A' * 70

        with self.assertRaises(ValidationError):
            category.full_clean()

    def test_category_string_representation(self):
        category = self.make_category(name='Name-cat')
        category.name = 'TESTEE'
        category.full_clean()
        category.save()
        self.assertEqual(
            str(category), 'TESTEE'
        )

    def test_get_absolute_url_return_right(self):
        self.recipe
        url = self.recipe.get_absolute_url()
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_save_method_cover_changed(self):
        image = Image.new("RGB", (100, 100), "white")
        image_bytes_io = io.BytesIO()
        image.save(image_bytes_io, format="JPEG")

        new_cover = SimpleUploadedFile(
            "new_cover.jpg",
            image_bytes_io.getvalue(),
            content_type="image/jpeg"
        )
        receita = Recipe(
            title='liltest',
            slug='tes-lil',
            preparation_time=1,
            servings=1
        )
        receita.save()
        receita.cover = new_cover
        receita.save()

        self.assertTrue(getattr(
            receita, 'cover_changed', True
        ))

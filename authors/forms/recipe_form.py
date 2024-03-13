from django import forms
from django.core.exceptions import ValidationError

from recipes.models import Recipe
from utils.placeholder import add_attr

from collections import defaultdict


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(
            self.fields.get('preparation_steps'), 'class', 'span-2'
        )

        add_attr(
            self.fields.get('cover'), 'class', 'span-2'
        )

    class Meta:
        model = Recipe
        fields = (
            'title', 'description', 'preparation_time',
            'preparation_time_unit', 'servings', 'servings_unit',
            'preparation_steps', 'cover',
        )
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                )
            ),
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cleaned_data = self.cleaned_data
        title = cleaned_data.get('title')
        preparation_time = int(cleaned_data.get('preparation_time'))
        servings = int(cleaned_data.get('servings'))

        if len(title) < 5:
            self._my_errors['title'].append(
                'O título deve ter pelo menos 5 caracteres'
            )

        if preparation_time is not None and preparation_time < 0:
            self._my_errors['preparation_time'].append(
                'O tempo de preparo não pode ser negativo'
            )

        if servings is not None and servings < 0:
            self._my_errors['servings'].append(
                'As porções não podem ter valor negativo'
            )

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean

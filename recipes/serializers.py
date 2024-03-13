from rest_framework import serializers

from collections import defaultdict

from .models import Recipe

from tag.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'public',
            'preparation', 'category', 'category_name',
            'author', 'author_name', 'tags', 'tag_objects',
            'tag_links', 'preparation_time', 'preparation_time_unit',
            'servings', 'servings_unit', 'preparation_steps', 'cover',
        ]
    public = serializers.BooleanField(
        source='is_published',
        read_only=True
    )
    preparation = serializers.SerializerMethodField(read_only=True)
    # primarykeyRelated mostra o ID
    # stringRelated mostra o Nome
    category_name = serializers.StringRelatedField(
        source='category'
    )
    author_name = serializers.StringRelatedField(
        source='author',
        read_only=True
    )
    tag_objects = TagSerializer(
        many=True,
        source='tags',
        read_only=True
    )
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        view_name='recipes:recipe_api_tag_v2',
        read_only=True
    )

    def get_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'

    def validate_title(self, value):
        title = value

        if len(title) < 5:
            raise serializers.ValidationError(
                'O campo precisa de pelo menos 5 caracteres!'
            )

        return title

    def validate(self, attrs):
        super_validate = super().validate(attrs)
        cleaned_data = attrs

        errors = defaultdict(list)

        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        preparation_time = int(cleaned_data.get('preparation_time'))
        servings = int(cleaned_data.get('servings'))

        if len(title) < 5:
            errors['title'].append(
                'O título deve ter pelo menos 5 caracteres'
            )

        if title == description:
            errors['title'].append(
                'O título não pode ser igual a descrição'
            )
            errors['description'].append(
                'A descrição não pode ser igual ao título'
            )

        if preparation_time is not None and preparation_time < 0:
            errors['preparation_time'].append(
                'O tempo de preparo não pode ser negativo'
            )

        if servings is not None and servings < 0:
            errors['servings'].append(
                'As porções não podem ter valor negativo'
            )

        if errors:
            raise serializers.ValidationError(errors)

        return super_validate

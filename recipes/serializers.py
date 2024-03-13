from rest_framework import serializers

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
            'tag_links'
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

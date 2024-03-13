from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Category

from tag.models import Tag


class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=50)
    slug = serializers.SlugField()


class RecipeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(
        max_length=65,
    )
    description = serializers.CharField(
        max_length=255,
    )
    public = serializers.BooleanField(
        source='is_published'
    )
    preparation = serializers.SerializerMethodField()
    # primarykeyRelated mostra o ID
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )
    # stringRelated mostra o Nome
    category_name = serializers.StringRelatedField(
        source='category'
    )
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    author_name = serializers.StringRelatedField(
        source='author'
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    tag_objects = TagSerializer(
        many=True,
        source='tags'
    )

    def get_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'

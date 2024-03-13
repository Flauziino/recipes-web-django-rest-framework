from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer, TagSerializer

from tag.models import Tag


@api_view()
def recipe_api_list(request):
    receitas = Recipe.objects.all().order_by('-id')[:10]
    receitas.select_related('category', 'author').prefetch_related('tags')
    serializador = RecipeSerializer(
        instance=receitas,
        many=True,
        context={'request': request}
    )
    return Response(serializador.data)


@api_view()
def recipe_api_detail(request, pk):
    receita = get_object_or_404(
        Recipe, pk=pk
    )
    receita.select_related('category', 'author').prefetch_related('tags')
    serializador = RecipeSerializer(
        instance=receita,
        many=False,
        context={'request': request}
    )
    return Response(serializador.data)


@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(
        Tag, pk=pk
    )
    serializador = TagSerializer(
        instance=tag,
        many=False,
        context={'request': request}
    )
    return Response(serializador.data)

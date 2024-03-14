from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from django.shortcuts import get_object_or_404

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer, TagSerializer

from tag.models import Tag


class RecipeAPIv2ViewSet(ModelViewSet):
    queryset = (
        Recipe.objects.filter(is_published=True)
        .order_by('-id')
    )
    queryset.select_related('author', 'category').prefetch_related('tags')
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination


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

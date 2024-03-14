# type: ignore
# flake8: noqa
# ARQUIVO DESTINADO A "GUARDAR" AS FUNCOES QUE FORAM REMOVIDAS PARA DAR
# ESPACO A CLASSES DENTRO DO CODIGO

# FUNCBASEVIEW DA LISTA DA INDEX PAGE
def index(request):

    receitas = (
        models.Recipe.objects.filter(is_published=True)
        .order_by('-id')
    )

    page_obj, pagination_range = make_pagination(
        request,
        receitas,
        PER_PAGE,
    )

    contexto = {
        'receitas': page_obj,
        'pagination_range': pagination_range,
    }

    return render(
        request,
        'recipes/index.html',
        contexto
    )


# FUNCBASEVIEW PARA VER/FILTRAR AS RECEITAS POR CATEGORIA
def category(request, category_id):

    receitas = get_list_or_404(
        models.Recipe.objects.filter(
            category__id=category_id,
            is_published=True
        ).order_by('-id')
    )

    for receita in receitas:
        category_name = receita.category.name

    page_obj, pagination_range = make_pagination(
        request,
        receitas,
        PER_PAGE,
    )

    contexto = {
        'receitas': page_obj,
        'title': f'{category_name}  - Category | ',
        'pagination_range': pagination_range,
    }

    return render(
        request,
        'recipes/category.html',
        contexto
    )


# FUNCBASEBIEW PARA DETALHE DA RECEITA
def recipe(request, id):

    receita = get_object_or_404(
        models.Recipe,
        id=id,
        is_published=True
    )

    contexto = {
        'receita': receita,
        'is_detail_page': True,
    }

    return render(
        request,
        'recipes/recipe-view.html',
        contexto
    )


# FUNCBASEVIEW PARA PESQUISA DE RECEITAS
def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    receitas = models.Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
        ), is_published=True
    ).order_by('id')

    page_obj, pagination_range = make_pagination(
        request,
        receitas,
        PER_PAGE,
    )

    contexto = {
        'page_title': f'Search for {search_term} | ',
        'search_term': search_term,
        'receitas': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}'
    }

    return render(
        request,
        'recipes/search.html',
        contexto
    )


###### API AGORA############
@api_view(http_method_names=['post', 'get'])
def recipe_api_list(request):
    if request.method == 'GET':
        receitas = Recipe.objects.all().order_by('-id')[:10]
        receitas.select_related('category', 'author').prefetch_related('tags')
        serializador = RecipeSerializer(
            instance=receitas,
            many=True,
            context={'request': request}
        )
        return Response(serializador.data)

    elif request.method == 'POST':
        # aqui drabalha-se igual um form django.
        serializador = RecipeSerializer(
            data=request.data
        )
        serializador.is_valid(raise_exception=True)
        serializador.save()
        return Response(
            serializador.data,
            status=status.HTTP_201_CREATED
        )


@api_view(http_method_names=['get', 'patch', 'delete'])
def recipe_api_detail(request, pk):
    receita = get_object_or_404(
        Recipe, pk=pk
    )
    if request.method == 'GET':
        serializador = RecipeSerializer(
            instance=receita,
            many=False,
            context={'request': request}
        )

        return Response(serializador.data)

    elif request.method == 'PATCH':
        serializador = RecipeSerializer(
            instance=receita,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True
        )
        serializador.is_valid(raise_exception=True)
        serializador.save()

        return Response(serializador.data)

    elif request.method == 'DELETE':
        receita.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

##### METODOS PADROES de uma CLASSBASEDVIEW API
((
    def get(self, request):
        receitas = (
            Recipe.objects.filter(is_published=True)
            .order_by('-id')[:10]
        )
        receitas.select_related('category', 'author').prefetch_related('tags')
        serializador = RecipeSerializer(
            instance=receitas,
            many=True,
            context={'request': request}
        )
        return Response(serializador.data)
    
    def patch(self, request, pk):
        receita = self.get_recipe(pk)
        serializador = RecipeSerializer(
            instance=receita,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True
        )
        serializador.is_valid(raise_exception=True)
        serializador.save()

        return Response(serializador.data)


    def post(self, request):
        # aqui drabalha-se igual um form django.
        serializador = RecipeSerializer(
            data=request.data
        )
        serializador.is_valid(raise_exception=True)
        serializador.save()
        return Response(
            serializador.data,
            status=status.HTTP_201_CREATED
        )
    
     def delete(self, request, pk):
        receita = self.get_recipe(pk)
        receita.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
))

# urls sem uso de router
path(
    'recipes/api/v2',
    api.RecipeAPIv2ViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }),
    name='recipes_api_v2'
),

path(
    'recipes/api/v2/<int:pk>/',
    api.RecipeAPIv2ViewSet.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'delete': 'destroy',
    }),
    name='recipe_api_detail_v2'
),
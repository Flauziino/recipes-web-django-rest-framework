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

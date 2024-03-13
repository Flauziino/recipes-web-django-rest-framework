from django.db.models import Q, F, Value
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Count
from django.db.models.functions import Concat

from recipes.models import Recipe


def theory(request, *args, **kwargs):
    receitas = Recipe.objects.all()
    # receita só sera usada quando eu utilizar o valor obtido

    # Ambos sao query/lista de objetos e podem utilizar de ".first() .last()"
    # ".order_by()"
    Recipe.objects.all() or Recipe.objects.filter()

    # Retorna apenas 1 obj, se nao existir vai levanter erro
    r = Recipe.objects.get()
    # Voce pode tratar com
    if not r:
        raise Http404
    # ou
    try:
        r = Recipe.objects.get()
    except ObjectDoesNotExist:
        r = None
    # ou por fim a melhor maneira ao meu ver
    r = get_object_or_404()
    # pois ja pega o objeto e caso nao encontre retorna 404

    # pode ser usado similar para o ".filter()" tb, e como proprio nome diz,
    # retorna uma lista
    r = get_list_or_404()

    # para fazer uma consulta utilizando o "Q" (que nos possibilita usar OR
    # nas consultas, com "|" ) é preciso
    # importar = from django.db.models import Q
    r = Recipe.objects.filter(
        Q(title__icontains='ola') |  # OU
        Q(description__icontains='ola') |
        Q(id__gte=1000)
    )

    # tem tambem uma consulta com o "F" (vem do mesmo local que o Q)
    # é como se fosse uma consulta assim:

    r = Recipe.objects.filter(
        id=F('author__id')
    )
    # significa que quero receitas onde o ID da receita é IGUAL ID do autor

    # quando quero um campo (ou campos) em especifico posso utilizar
    # ".values()" e retorna um dict
    r = Recipe.objects.values(
        'id', 'title', 'author'
    )

    # temos as consultas ONLY e DEFER tb (perigosas), ONLY é igual a .values()
    # porem ele retorna DIRETO um objeto de query
    r = Recipe.objects.only(
        'id', 'title', 'author'
    )
    # ONLY retorna os campos selecionados
    r = Recipe.objects.defer(
        'id', 'title', 'author'
    )
    # DEFER exclui da busca os campos selecionados

    # tem o aggregatefunc tb, que sao as func de agregacao do django
    # como count, sum, min, max, avg......
    n = Recipe.objects.aaggregate(Count('id'))
    # podemos criar um nome completo pro usuario com ANNOTATE da seguinte forma
    r = Recipe.objects.all().annotate(
        author_full_name=Concat(
            F('author__first_name'), Value(' '),
            F('author__last_name'), Value(' ('),
            F('author__username'), Value(')'),
        )
    )

    # porem seria melhor criar um metodo dentro do seu proprio model,
    # por exemplo um "get_author_full_name"
    # ficaria escrito dessa forma.
    # supondo que estou criando esse metodo dentro de um model Receita
    # que tem foreingkey de autores.
    def get_author_full_name(self):
        first_name = self.author.first_name
        last_name = self.author.last_name
        full_name = f'{first_name} {last_name}'
        return full_name

    contexto = {
        'receitas': receitas,
        'numero': n['id__count'],
        'numero_2': n.value()
    }

    return render(
        request,
        'recipes/index.html',
        contexto
    )

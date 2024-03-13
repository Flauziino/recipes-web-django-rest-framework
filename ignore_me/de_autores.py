# type: ignore
# flake8: noqa
# ARQUIVO DESTINADO A "GUARDAR" AS FUNCOES QUE FORAM REMOVIDAS PARA DAR
# ESPACO A CLASSES DENTRO DO CODIGO


# FUNCBASEDVIEW PARA LER/EDITAR UMA RECEITA
@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_edit(request, id):
    receita = get_object_or_404(
        Recipe,
        is_published=False,
        author=request.user,
        pk=id
    )

    form = AuthorRecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
        instance=receita
    )

    if form.is_valid():
        receita = form.save(commit=False)

        receita.author = request.user
        receita.preparation_steps_is_html = False
        receita.is_published = False

        receita.save()

        messages.success(
            request, 'Sua receita foi salva com sucesso!'
        )
        return redirect(
            reverse('authors:dashboard_edit', args=(id,))
        )

    contexto = {
        'form': form
    }

    return render(
        request,
        'author/dashboard_recipe.html',
        contexto
    )


# FUNCBASEVIEW PARA CRIAR UMA NOVA RECEITA
@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_create(request):

    if request.method == 'POST':
        form = AuthorRecipeForm(
            data=request.POST,
            files=request.FILES
        )

        if form.is_valid():
            form.save(commit=False)

            nova_receita = Recipe.objects.create(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                preparation_time=form.cleaned_data['preparation_time'],
                preparation_time_unit=form.cleaned_data['preparation_time_unit'],  # noqa: E501
                servings=form.cleaned_data['servings'],
                servings_unit=form.cleaned_data['servings_unit'],
                preparation_steps=form.cleaned_data['preparation_steps'],
                cover=form.cleaned_data['cover'],
            )

            nova_receita.author = request.user
            nova_receita.preparation_steps_is_html = False
            nova_receita.is_published = False

            nova_receita.save()

            messages.success(
                request, 'Sua receita foi salva com sucesso!'
            )

            return redirect('authors:dashboard')

    else:
        form = AuthorRecipeForm()

    contexto = {
        'form': form,
    }

    return render(
        request,
        'author/dashboard_new_recipe.html',
        contexto
    )


# FUNCBASEVIEW PARA DELETAR RECEITAS
@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_delete(request):
    if not request.POST:
        raise Http404

    POST = request.POST
    id = POST.get('id')

    receita = get_object_or_404(
        Recipe,
        is_published=False,
        author=request.user,
        pk=id
    )

    receita.delete()
    messages.success(
        request, 'Receita apagada com sucesso!'
    )

    return redirect(
        reverse('authors:dashboard')
    )

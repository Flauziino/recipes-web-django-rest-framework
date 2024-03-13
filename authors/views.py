from django.views import View
from django.http import Http404
from django.urls import reverse
from django.contrib import messages
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404

from .models import Profile
from recipes.models import Recipe
from .forms import RegisterForm, LoginForm, AuthorRecipeForm


def register_view(request):
    form = RegisterForm()

    contexto = {
        'form': form,
        'form_action': reverse('authors:create')
    }

    return render(
        request,
        'author/register_view.html',
        contexto
    )


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()

        messages.success(
            request,
            'Cadastro realizado com sucesso!'
        )

        del (request.session['register_form_data'])

        return redirect(
            reverse('authors:login')
        )

    contexto = {
        'form': form
    }

    messages.error(
        request,
        'Existem erros em seu formulário, favor conferir os dados.'
    )

    return render(
        request,
        'author/register_view.html',
        contexto
    )


def login_view(request):
    form = LoginForm

    contexto = {
        'form': form,
        'form_action': reverse('authors:login_create')
    }
    return render(
        request,
        'author/login.html',
        contexto
    )


def login_create(request):
    if not request.POST:
        raise Http404

    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(
                request, 'Logado com sucesso!'
            )
            login(request, authenticated_user)

            return redirect('authors:dashboard')

        messages.error(
            request, 'Falha ao logar, usuário ou senha inválidos'
        )
        return redirect('authors:login')

    messages.error(
        request, 'Falha ao logar, usuário ou senha inválidos'
    )
    return redirect('authors:login')


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:

        messages.error(
            request, 'Você precisa estar logado para realizar esta ação'
        )

        return redirect(
            reverse('authors:login')
        )

    if request.POST.get('username') != request.user.username:
        messages.error(
            request, 'Este usuário não tem acesso a esta página'
        )

        return redirect(
            reverse('authors:login')
        )

    logout(request)
    messages.success(
        request, 'Deslogado com sucesso!'
    )

    return redirect(
        reverse('authors:login')
    )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    receitas = Recipe.objects.filter(
        is_published=False,
        author=request.user
    )

    contexto = {
        'receitas': receitas
    }

    return render(
        request,
        'author/dashboard.html',
        contexto
    )


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardRecipeEdit(View):
    def get_recipe(self, id):
        receita = None

        if id:
            receita = get_object_or_404(
                Recipe,
                is_published=False,
                author=self.request.user,
                pk=id
            )

        return receita

    def render_recipe(self, form):
        contexto = {
            'form': form
        }

        return render(
            self.request,
            'author/dashboard_recipe.html',
            contexto
        )

    def get(self, request, id):
        receita = self.get_recipe(id)
        form = AuthorRecipeForm(instance=receita)
        return self.render_recipe(form)

    def post(self, request, id):
        receita = self.get_recipe(id)

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

        return self.render_recipe(form)


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardRecipeCreate(View):
    def render_form(self, form):
        contexto = {
            'form': form,
        }

        return render(
            self.request,
            'author/dashboard_new_recipe.html',
            contexto
        )

    def get(self, request):
        form = AuthorRecipeForm()
        return self.render_form(form)

    def post(self, request):
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

        messages.error(
            request, 'Existem erros em seu formulário!'
        )

        return self.render_form(form)


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardRecipeDelete(DashboardRecipeEdit):
    def post(self, *args, **kwargs):
        receita = self.get_recipe(
            self.request.POST.get('id')
        )
        receita.delete()
        messages.success(
            self.request, 'Receita apagada com sucesso!'
        )
        return redirect(
            reverse('authors:dashboard')
        )


class ProfileView(TemplateView):
    template_name = 'author/profile.html'

    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(**kwargs)
        profile_id = ctx.get('id')
        profile = get_object_or_404(
            Profile.objects.filter(
                pk=profile_id
            ).select_related('author'),
            pk=profile_id
        )

        return self.render_to_response({
            **ctx,
            'perfil': profile,
        })

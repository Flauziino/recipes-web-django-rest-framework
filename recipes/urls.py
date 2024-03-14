from django.urls import path

from recipes.views import site, api

from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


recipe_api_v2_router = SimpleRouter()
recipe_api_v2_router.register(
    'recipes/api/v2',
    api.RecipeAPIv2ViewSet,
    basename='recipes-api'
)

app_name = 'recipes'

# urls do app recipes
urlpatterns = [
    path(
        '',
        site.RecipeListIndexView.as_view(),
        name='index'
    ),

    path(
        'recipes/search',
        site.RecipeListSearchView.as_view(),
        name='search'
    ),

    path(
        'recipes/tags/<slug:slug>/',
        site.RecipeListTagView.as_view(),
        name="tag"
    ),

    path(
        'recipes/category/<int:category_id>/',
        site.RecipeListCategoryView.as_view(),
        name='category'
    ),

    path(
        'recipes/<int:pk>',
        site.RecipeDetailView.as_view(),
        name='recipe'
    ),

    # URL PARA ENTREGA DE API EXEMPLO
    path(
        'recipes/api/v1/',
        site.RecipeListIndexViewApi.as_view(),
        name='recipes_api'
    ),

    path(
        'recipes/api/v1/<int:pk>',
        site.RecipeDetailViewApi.as_view(),
        name='recipe_api_detail'
    ),

    # URLS PARA ENTREGA DE API TRUE

    path(
        'recipes/api/v2/tag/<int:pk>/',
        api.tag_api_detail,
        name='recipe_api_tag_v2'
    ),

    # JWT
    path(
        'recipes/api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'recipes/api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'recipes/api/token/verify/',
        TokenVerifyView.as_view(),
        name='token_verify'
    ),
    # Por último
]

urlpatterns += recipe_api_v2_router.urls

from django.urls import path
from .views import site, api

from rest_framework.routers import SimpleRouter

app_name = 'authors'

author_api_router = SimpleRouter()
author_api_router.register(
    'api',
    api.AuthorAPIv2ViewSet,
    basename='author-api'
)

urlpatterns = [
    path('register/', site.register_view, name='register'),
    path('register/create/', site.register_create, name='create'),

    path('login/', site.login_view, name='login'),
    path('login/login-create', site.login_create, name='login_create'),

    path('logout/', site.logout_view, name='logout'),

    path('dashboard/', site.dashboard, name='dashboard'),
    # create
    path(
        'dashboard/recipe/create',
        site.DashboardRecipeCreate.as_view(),
        name='dashboard_create'
    ),
    # delete
    path(
        'dashboard/recipe/delete',
        site.DashboardRecipeDelete.as_view(),
        name='dashboard_delete'
    ),
    # update/read
    path(
        'dashboard/recipe/<int:id>/edit',
        site.DashboardRecipeEdit.as_view(),
        name='dashboard_edit'
    ),

    # profile
    path(
        'profile/<int:id>/',
        site.ProfileView.as_view(),
        name='profile'
    ),

]

urlpatterns += author_api_router.urls

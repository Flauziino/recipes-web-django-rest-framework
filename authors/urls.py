from django.urls import path
from . import views


app_name = 'authors'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='create'),

    path('login/', views.login_view, name='login'),
    path('login/login-create', views.login_create, name='login_create'),

    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    # create
    path(
        'dashboard/recipe/create',
        views.DashboardRecipeCreate.as_view(),
        name='dashboard_create'
    ),
    # delete
    path(
        'dashboard/recipe/delete',
        views.DashboardRecipeDelete.as_view(),
        name='dashboard_delete'
    ),
    # update/read
    path(
        'dashboard/recipe/<int:id>/edit',
        views.DashboardRecipeEdit.as_view(),
        name='dashboard_edit'
    ),

    # profile
    path(
        'profile/<int:id>/',
        views.ProfileView.as_view(),
        name='profile'
    ),

]

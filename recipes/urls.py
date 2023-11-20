# recipes/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recipes/', views.recipe_all, name='recipe_all'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/new/', views.recipe_new, name='recipe_new'),
    path('recipe/<int:pk>/edit/', views.recipe_edit, name='recipe_edit'),
    path('recipe/<int:pk>/delete/', views.recipe_delete, name='recipe_delete'),
    path('search/', views.recipe_search, name='recipe_search'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
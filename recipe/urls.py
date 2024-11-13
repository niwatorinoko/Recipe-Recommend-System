from django.contrib import admin
from django.urls import path, include
from recipe.views import RecipeSearchView, RecipesListView, RecipesCreateView, DiaryCreateView, DiaryDetailView, DiaryDeleteView


app_name = 'recipe'

urlpatterns = [
    path('', RecipesListView.as_view(), name='list'),
    path('recipe-search/', RecipeSearchView.as_view(), name='recipe_search'),
    path('create/', RecipesCreateView.as_view(), name='create'),
    path('create-diary/<int:recipe_id>/', DiaryCreateView.as_view(), name='create_diary'),
    path('diary/<int:pk>/', DiaryDetailView.as_view(), name='diary_detail'),
    path('delete-diary/<int:pk>', DiaryDeleteView.as_view(), name='delete_diary'),
]
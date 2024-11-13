from django.contrib import admin
from django.urls import path, include
from recipe.views import RecipeSearchView


app_name = 'recipe'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recipe-search/', RecipeSearchView.as_view(), name='recipe_search'),
    #path('', RecipesListView.as_view(), name='list'),
    # path('detail/<int:pk>', PostsDetailView.as_view(), name='detail'),
    # path('create', PostsCreateView.as_view(), name='create'),
    # path('delete/<int:pk>', PostsDeleteView.as_view(), name='delete'),
]
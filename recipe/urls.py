from django.urls import path
from recipe.views import RecipesListView, RecipesCreateView, DiaryCreateView, DiaryDetailView, DiaryDeleteView


app_name = 'recipe'

urlpatterns = [
    path('', RecipesListView.as_view(), name='list'),
    path('create/', RecipesCreateView.as_view(), name='create'),
    path('create-diary/<int:recipe_id>/', DiaryCreateView.as_view(), name='create_diary'),
    path('diary/<int:pk>/', DiaryDetailView.as_view(), name='diary_detail'),
    path('delete-diary/<int:pk>', DiaryDeleteView.as_view(), name='delete_diary'),
]
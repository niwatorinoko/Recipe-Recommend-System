from django.shortcuts import render, redirect, reverse
from reciperecommendsystem.settings import GOOGLE_API_KEY
from rest_framework.views import APIView
import google.generativeai as genai
from .models import Recipe, Diary
import markdown
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

class AuthorOnly(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        """
        投稿の作者とログインしてるユーザーが同じかどうか判定する
        """
        diary = self.get_object()
        return diary.author == self.request.user
    
    def handle_no_permission(self):
        """
        test_funcでFalseだった場合特定のページにリダイレクトする
        """
        return reverse('authentications:profile', kwargs={'pk': self.request.user.pk})
    

class RecipesListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipe/recipes_list.html'
    context_object_name = 'recipes'
    paginate_by = 5  # ページネーションの1ページあたりのアイテム数

    def get_queryset(self):
        queryset = Recipe.objects.order_by('-created_at')
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(recipe_info__icontains=keyword)  # レシピ情報にキーワードを含むレシピを検索
        return queryset


# input : user_ingredients, weather, mood, budget, num_people
# output : title, recipe_ingredients, instructions, nutrition_info, preparation_time, budget, num_people    
class RecipeSearchView(APIView):
    def get(self, request):
        return render(request, 'recipe/recipe_search.html')

    def post(self, request):
        # フォームからのユーザー入力を取得
        user_ingredients = request.POST.get('user_ingredients')
        weather = request.POST.get('weather')
        mood = request.POST.get('mood')
        budget = request.POST.get('budget')
        num_people = request.POST.get('num_people')

        # Google Generative AIの設定
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")

        # プロンプト作成
        prompt = f"""
        I want to make One recipe with {user_ingredients} that is {mood}, suitable for a {weather} day,
        serves {num_people} people, and costs {budget} NTD.
        """

        response = model.generate_content(prompt)
        recipe_info = markdown.markdown(response.text)

        # 結果をテンプレートに渡す
        context = {
            'recipe_info': recipe_info,
            'user_ingredients': user_ingredients,
            'weather': weather,
            'mood': mood,
            'budget': budget,
            'num_people': num_people,
            'recipe_info': recipe_info,
        }
        return render(request, 'recipe/recipe_search.html', context)
    

class RecipesCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    template_name = 'recipe/recipes_create.html'
    fields = ['user_ingredients', 'weather', 'mood', 'budget', 'num_people']
    success_url = reverse_lazy('recipe:list')

    def form_valid(self, form):
        # フォームからのユーザー入力を取得
        form.instance.author = self.request.user
        user_ingredients = form.cleaned_data['user_ingredients']
        weather = form.cleaned_data['weather']
        mood = form.cleaned_data['mood']
        budget = form.cleaned_data['budget']
        num_people = form.cleaned_data['num_people']

        # Google Generative AIの設定
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # プロンプト作成
        prompt = f"""
        Please suggest a creative, original recipe using the ingredients: {user_ingredients}. 
        The recipe should be {mood}, suitable for a {weather} day, serve {num_people} people, 
        and stay within a budget of {budget} NTD. Please think  title, recipe_ingredients, instructions, nutrition_info, preparation_time, budget.
        Avoid using copyrighted text.
        """

        # AIからレシピ情報を生成
        response = model.generate_content(prompt)
        recipe_info = markdown.markdown(response.text) if response else "No recipe found."

        # レシピ情報を保存
        form.instance.recipe_info = recipe_info
        self.object = form.save()

        # レシピ生成後、DiaryCreateViewにリダイレクト
        return redirect(reverse('recipe:create_diary', kwargs={'recipe_id': self.object.id}))

class DiaryCreateView(LoginRequiredMixin, CreateView):
    model = Diary
    template_name = 'recipe/diary_create.html'
    fields = ['rating', 'comments']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe_id = self.kwargs.get('recipe_id')
        context['recipe'] = Recipe.objects.get(id=recipe_id)
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        recipe_id = self.kwargs.get('recipe_id')
        recipe = Recipe.objects.get(id=recipe_id)
        form.instance.recipe = recipe
        form.instance.user_ingredients = recipe.user_ingredients
        form.instance.weather = recipe.weather
        form.instance.mood = recipe.mood
        form.instance.budget = recipe.budget
        form.instance.num_people = recipe.num_people
        form.instance.recipe_info = recipe.recipe_info
        self.object = form.save()
        return redirect('recipe:diary_detail', pk=self.object.id)

class DiaryDetailView(DetailView):
    model = Diary
    template_name = 'recipe/diary_detail.html'
    context_object_name = 'diary'

    def get_object(self):
        # `pk` に基づいて Diary オブジェクトを取得
        diary_id = self.kwargs.get('pk')
        return get_object_or_404(Diary, pk=diary_id)


class DiaryDeleteView(AuthorOnly, DeleteView):
    """
    Diary を削除するためのビュー
    """
    model = Diary
    template_name = 'recipe/diary_delete.html'
    context_object_name = 'diary'
    # success_url = reverse_lazy('authentications:profile')

    def get_object(self, queryset=None):
        """
        Diary オブジェクトを取得し、削除の権限があるか確認
        """
        diary_id = self.kwargs.get('pk')
        return get_object_or_404(Diary, pk=diary_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe_info'] = self.object.recipe.recipe_info
        return context

    def get_success_url(self):
        # 現在ログインしているユーザーのプロフィールページにリダイレクト
        return reverse('authentications:profile', kwargs={'pk': self.request.user.pk})

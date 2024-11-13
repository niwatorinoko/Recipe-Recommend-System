from django.shortcuts import render
from reciperecommendsystem.settings import GOOGLE_API_KEY
from rest_framework.views import APIView
import google.generativeai as genai
from .models import Recipe
import markdown
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

class RecipesListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipe/recipes_list.html'

    def get_queryset(self):
        return Recipe.objects.order_by('-created_at')

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
        recipe_info = response.text

        html_content = markdown.markdown(recipe_info)
        # 結果をテンプレートに渡す
        context = {
            'recipe_info': recipe_info,
            'user_ingredients': user_ingredients,
            'weather': weather,
            'mood': mood,
            'budget': budget,
            'num_people': num_people,
        }
        return render(request, 'recipe/recipe_search.html', {'content': html_content})
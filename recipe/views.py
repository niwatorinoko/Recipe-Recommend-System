from django.shortcuts import render
from reciperecommendsystem.settings import GOOGLE_API_KEY
from rest_framework.views import APIView
import google.generativeai as genai
from .models import Recipe

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
        Use this JSON schema:
        Recipe = {{
            'recipe_name': str, 'ingredients': list[str], 'instructions': list[str],
            'nutrition_info': dict, 'preparation_minutes': int, 'budget': int, 'num_people': int
        }}
        Return: list[Recipe]
        """
        # プロンプト作成
        # prompt = f"""
        #  {user_ingredients} の材料のみ使って、 {mood} 、 {weather} 、 {num_people} 人、 予算は{budget} NTD.で作れるレシピを1つ教えてください。
        # Use this JSON schema:
        # Recipe = {{
        #     'recipe_name': str, 'ingredients': list[str], 'instructions': list[str],
        #     'nutrition_info': dict, 'preparation_time': int, 'budget': int, 'num_people': int
        # }}
        # Return: list[Recipe]
        # """
        response = model.generate_content(prompt)
        # Recipe.recipe_info = response.text
        recipe_info = response.text

        # 結果をテンプレートに渡す
        context = {
            'recipe_info': recipe_info,
            'user_ingredients': user_ingredients,
            'weather': weather,
            'mood': mood,
            'budget': budget,
            'num_people': num_people,
        }
        return render(request, 'recipe/recipe_search.html', context)
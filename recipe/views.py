from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.shortcuts import get_object_or_404, redirect, reverse
from django.urls import reverse_lazy
from reciperecommendsystem.settings import RECIPE_TEXT_API_KEY, RECIPE_IMAGE_API_KEY
import google.generativeai as genai
import markdown
import replicate
import requests
from django.core.files.base import ContentFile
from .models import Recipe, Diary

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
        weather = self.request.GET.get('weather')
        mood = self.request.GET.get('mood')
        budget = self.request.GET.get('budget')
        num_people = self.request.GET.get('num_people')
        rating = self.request.GET.get('rating')

        # キーワード検索
        if keyword:
            queryset = queryset.filter(recipe_info__icontains=keyword)
        # 天気で絞り込み
        if weather:
            queryset = queryset.filter(weather__iexact=weather)
        # 気分で絞り込み
        if mood:
            queryset = queryset.filter(mood__iexact=mood)
        # 予算で絞り込み
        if budget:
            queryset = queryset.filter(budget__lte=budget)
        # 人数で絞り込み
        if num_people:
            queryset = queryset.filter(num_people__gte=num_people)
        # 評価で絞り込み
        if rating:
            queryset = queryset.filter(diary__rating=rating)

        return queryset



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
        genai.configure(api_key=RECIPE_TEXT_API_KEY)
        gemini_model = genai.GenerativeModel("gemini-1.5-flash")

        # レシピ生成プロンプト作成
        prompt = f"""
        Please suggest a creative, original recipe using the ingredients: {user_ingredients}. 
        The recipe should be {mood}, suitable for a {weather} day, serve {num_people} people, 
        and stay within a budget of {budget} NTD. Please think title, recipe_ingredients, instructions, nutrition_info, preparation_time, budget.
        Avoid using copyrighted text. Please write in zh-tw.
        """

        # AIからレシピ情報を生成
        response = gemini_model.generate_content(prompt)
        recipe_info = markdown.markdown(response.text) if response else "No recipe found."
        form.instance.recipe_info = recipe_info

        # ReplicateのStable Diffusionモデルを使用して画像生成
        replicate_client = replicate.Client(api_token=RECIPE_IMAGE_API_KEY)
        model = replicate_client.models.get("stability-ai/stable-diffusion")
        version = model.versions.list()[0]  # 最新バージョンを使用

        # 画像生成プロンプトの作成
        image_prompt = f"A delicious dish described as follows: {recipe_info[:200]}..."

        # AI画像生成リクエスト
        try:
            prediction = replicate_client.predictions.create(
                version=version.id,
                input={"prompt": image_prompt}
            )
            prediction = replicate_client.predictions.get(prediction.id)

            # 完了するまで待つ
            while prediction.status not in ["succeeded", "failed"]:
                prediction.reload()

            if prediction.status == "succeeded":
                image_url = prediction.output[0]
            else:
                image_url = None
        except Exception as e:
            print(f"Error generating image: {e}")
            image_url = None

        # 画像を保存
        if image_url:
            response = requests.get(image_url)
            if response.status_code == 200:
                form.instance.recipe_image.save(
                    f"recipe_{form.instance.id}.png", ContentFile(response.content)
                )
        else:
            # デフォルト画像を設定
            with open('static/images/sample/sample1.png', 'rb') as f:
                form.instance.recipe_image.save(
                    "sample1.png", ContentFile(f.read())
                )

        # フォーム保存
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

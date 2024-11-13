from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class Common(models.Model):
    """
    共通フィールドを持つ抽象モデル
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')

    class Meta:
        abstract = True


class Recipe(Common):
    """
    レシピモデル
    """
    # user input :weather, mood, budget, num_people
    user_ingredients = models.TextField(verbose_name='User Ingredients', blank=True)
    weather = models.CharField(max_length=50, verbose_name='Weather', blank=True)
    mood = models.CharField(max_length=50, verbose_name='Mood', blank=True)
    budget = models.IntegerField(verbose_name='Budget (NTD)', null=True, blank=True)
    num_people = models.IntegerField(verbose_name='Serving Size', null=True, blank=True)
    # response
    recipe_info = models.TextField(verbose_name='Recipe Info', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('recipes:detail', kwargs={'pk': self.pk})

class Diary(Common):
    """
    日記モデル
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Recipe', null=True, blank=True)
    rating = models.IntegerField(verbose_name='Rating', null=True, blank=True)
    comments = models.TextField(verbose_name='Comments', blank=True, null=True)
    
    # 日記としての追加フィールド
    rating = models.IntegerField(verbose_name='Rating', null=True, blank=True)
    comments = models.TextField(verbose_name='Comments', blank=True, null=True)


    def get_absolute_url(self):
        return reverse('recipe:diary_detail', kwargs={'pk': self.pk})
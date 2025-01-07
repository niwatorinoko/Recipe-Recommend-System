from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import FormView, View, DetailView, UpdateView, TemplateView, ListView
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse
from .forms import UserCreationForm, UserLoginForm, UserUpdateForm
from recipe.models import Diary, Recipe
from django.views.generic import TemplateView

User = get_user_model()


class UnauthenticatedOnly(UserPassesTestMixin):
    """
    ログイン済みのユーザーのアクセスを制限する
    """
    def test_func(self):
        # ログイン状態じゃないかチェック
        return not self.request.user.is_authenticated
    
    def handle_no_permission(self):
        # ログイン状態なら投稿一覧へリダイレクト
        return redirect('authentications:index')
    
class AuthenticationsSignupView(UnauthenticatedOnly, FormView):
    """ 
    ユーザーの登録フォームをHTMLに渡す
    """
    template_name = 'authentications/authentications_signup.html'
    form_class = UserCreationForm

    def post(self, request, *args, **kwargs):
        """ 
        Postリクエスト時の処理
        Userモデルのフォームを検証し、データを保存する
        検証成功すればindexにリダイレクトし、自動でログインした状態にする
        検証失敗すれば登録ページを返す
        """
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()

            # 保存後に認証を実行してログイン
            user = authenticate(email=user_form.cleaned_data['email'], password=user_form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('authentications:index')
            else:
                print("Authentication failed")  # 認証失敗時
                # 認証が失敗した場合はエラーメッセージを表示
                return redirect('authentications:signup')
        else:
            print("Form is not valid:", user_form.errors)  # 検証エラーの詳細を表示
            return render(request, self.template_name, {'form': user_form})

class AuthenticationsLoginView(UnauthenticatedOnly ,FormView):
    """ 
    ログインフォームを渡す
    """
    template_name = 'authentications/authentications_login.html'
    form_class = UserLoginForm

    def post(self, request, *args, **kwargs):
        """ 
        Postリクエスト時の処理
        送信されたメールアドレスとパスワードでユーザーを検索し見つかったらログインする
        見つからなかったらログインページを返す
        """
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('authentications:login')
        return redirect('authentications:login')

class AuthenticationsLogoutView(View):
    """
    ログアウト機能 HTMLファイルはなし
    """
    def get(self, request):
        logout(request)
        return redirect('authentications:login')


class UserProfileView(DetailView):
    """
    特定のユーザーの投稿一覧（日記）を取得してHTMLを返すビュー
    """
    model = User
    template_name = 'authentications/user_profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 現在のユーザー（プロフィール）の日記を取得
        user_diary = Diary.objects.filter(author=self.object).select_related('recipe').order_by('-created_at')
        context['user_diary'] = user_diary
        return context


class AuthenticationsUpdateView(LoginRequiredMixin, UpdateView):
    """
    ユーザーのプロフィール情報を更新するためのビュー
    """
    model = User
    form_class = UserUpdateForm
    template_name = 'authentications/authentications_update.html'

    def get_object(self, queryset=None):
        """ログイン中のユーザーのみが自分の情報を編集可能"""
        return self.request.user

    def form_valid(self, form):
        """フォームが有効な場合、保存してリダイレクト"""
        self.object = form.save()
        return redirect(reverse('authentications:profile', kwargs={'pk': self.object.pk}))
    

class IndexView(TemplateView):
    """
    トップページを表示するビュー
    """
    template_name = 'authentications/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 最新の 4 つのレシピを取得
        context['latest_recipes'] = Recipe.objects.order_by('-created_at')[:4]
        return context


class DiarySearchView(ListView):
    """
    ユーザー名で検索し、公開プロフィールの日記を表示するビュー
    """
    template_name = 'authentications/diary_search.html'

    def get(self, request, *args, **kwargs):
        username = request.GET.get('username', None)

        if not username:
            return render(request, self.template_name, {'error': 'Please provide a username.'})
        
        try:
            # ユーザーを取得、存在しない場合エラーメッセージを渡す
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, self.template_name, {'error': 'No user matches the given username.'})

        # プロフィールが非公開の場合
        if not user.is_profile_public:
            return render(request, self.template_name, {'error': 'This profile is private.'})

        # 公開されているユーザーの日記を取得
        user_diary = Diary.objects.filter(author=user).select_related('recipe').order_by('-created_at')

        return render(request, self.template_name, {
            'user': user,
            'user_diary': user_diary
        })
    
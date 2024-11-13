from django.views import generic
from django.shortcuts import render, redirect
from django.views.generic import FormView, View, DetailView, TemplateView
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from .forms import UserCreationForm, UserLoginForm

User = get_user_model()

class IndexView(generic.TemplateView):
    template_name = 'authentications/index.html'

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
        検証成功すれば投稿一覧ページにリダイレクトし、自動でログインした状態にする
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
            return redirect('authentications:index')
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
    特定のユーザーの投稿一覧を取得しHTMLを返す
    """
    model = User
    template_name = 'authentications/user_profile.html'

    def get(self, request, pk):
        user = User.objects.get(id=pk)
        context = {
            'user': user,
        }
        return render(request, self.template_name, context)
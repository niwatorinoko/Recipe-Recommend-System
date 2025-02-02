from django.urls import path
from .views import AuthenticationsSignupView, AuthenticationsLoginView, AuthenticationsLogoutView, UserProfileView, AuthenticationsUpdateView, IndexView, DiarySearchView

app_name = 'authentications'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('signup/', AuthenticationsSignupView.as_view(), name='signup'),
    path('login/', AuthenticationsLoginView.as_view(), name='login'),
    path('logout/', AuthenticationsLogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
    path('profile/edit/', AuthenticationsUpdateView.as_view(), name='edit'),
    path('diary-search/', DiarySearchView.as_view(), name='diary_search'),
]
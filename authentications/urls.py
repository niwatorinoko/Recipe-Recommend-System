from django.urls import path
from .views import IndexView, AuthenticationsSignupView, AuthenticationsLoginView, AuthenticationsLogoutView, UserProfileView

app_name = 'authentications'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('signup/', AuthenticationsSignupView.as_view(), name='signup'),
    path('login/', AuthenticationsLoginView.as_view(), name='login'),
    path('logout/', AuthenticationsLogoutView.as_view(), name='logout'),
    path('profile/<int:pk>', UserProfileView.as_view(), name='profile'),
]
#http://0.0.0.0:8000/accounts/
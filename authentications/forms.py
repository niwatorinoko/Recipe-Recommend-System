from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    username = forms.CharField(label='Name', widget=forms.TextInput(
        attrs={'style': 'margin-bottom: 30px; margin-left: 10px; width: 93%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;'}
    ))

    email = forms.EmailField(label='Email Address', widget=forms.TextInput(
        attrs={'style': 'margin-bottom: 30px; margin-left: 10px; width: 93%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;'}
    ))

    password = forms.CharField(label='Password', min_length=8, widget=forms.PasswordInput(attrs={'style': 'margin-bottom: 30px; margin-left: 10px; width: 93%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;'}))
    confirm_password = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'style': 'margin-bottom: 30px; margin-left: 10px; width: 93%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;'}))


    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password')
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('Password does not match')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        user.set_password(password)  # パスワードをハッシュ化して設定

        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', 'is_staff', 'is_superuser', 'is_active')

    def clean_password(self):
        return self.initial['password']


class UserLoginForm(forms.Form):
    email = forms.EmailField(label='E-mail address', widget=forms.TextInput(
        attrs={
            'class': 'input mb-4',
            'placeholder': 'E-mail address'
        }
    ))

    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': 'input mb-4',
            'placeholder': 'Password'
        }
    ))
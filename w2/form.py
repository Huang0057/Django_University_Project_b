from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Example', 'class': "sign_username", 'required': 'required'}),
            'email': forms.EmailInput(attrs={'placeholder': 'example@email.com', 'class': "sign_email", 'required': 'required'}),
            'password': forms.PasswordInput(attrs={'placeholder': '********', 'id': 'id_password', 'class': "sign_Password", 'autocomplete': 'on', 'required': 'required'})
        }

        labels = {
            'username': '使用者名稱',
            'email': '電子郵件',
            'password': '密碼'
        }


class LoginForm(forms.Form):
    username = forms.CharField(label='帳號', widget=forms.TextInput(
        attrs={'class': 'login_username'}))
    password = forms.CharField(label='密碼', widget=forms.PasswordInput(
        attrs={'class': 'login_Password'}))
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['USER_UID', 'Arm_UID', 'Foot_UID', 'Limb_UID', 'Hand_UID', 'TotalCoin']
from django import forms
from django.contrib.auth.models import User

from .models import Profile


class UserCreateForm(forms.ModelForm):
    """Форма для редактирования профиля"""
    class Meta:
        model = User
        fields = ['first_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    """Форма для редактирования профиля"""
    class Meta:
        model = Profile
        fields = ['description', 'avatar']

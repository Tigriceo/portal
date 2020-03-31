from django import forms
from django.contrib.auth.models import User

from .models import Profile


# class UserCreateForm(forms.ModelForm):
#
#     class Meta:
#         model = User
#         fields = ['username']


class ProfileUpdateForm(forms.ModelForm):
    """Форма для редактирования профиля"""
    class Meta:
        model = Profile
        fields = ['description', 'phone_number']

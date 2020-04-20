from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, View, CreateView, FormView
from string import digits
from random import choice
from django.contrib.auth.hashers import make_password

from service.smsru.core import send_sms_ru
from .models import Profile
from .forms import ProfileUpdateForm
from offerboard.views import CalculateProfile


class RegistrationView(View):
    """Регистрация и авторизация"""
    def post(self, request):
        username = request.POST.get("username")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User()
            user.username = username
        code = list()
        for i in range(4):
            code.append(choice(digits))
        hashed_pin = make_password(''.join(code))
        pin = ''.join(code)
        print(pin)
        user.password = hashed_pin
        user.save()
        print(send_sms_ru(username, pin))
        return HttpResponse(status=201)


class ProfileView(LoginRequiredMixin, CalculateProfile, UpdateView):
    """Профиль пользователя"""
    form_class = ProfileUpdateForm
    template_name = 'myprofile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        obj = get_object_or_404(Profile, user=self.request.user)
        return obj

    # def get_object(self, queryset=None):
    #     return self.request.user.profile

    def form_valid(self, form):
        return super().form_valid(form)


class LogOutView(View):
    """Выход из профиля"""
    def get(self, request):
        logout(self.request)
        return redirect('/')



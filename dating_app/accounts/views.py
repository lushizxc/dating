from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sessions.backends.base import VALID_KEY_CHARS
from django.dispatch import receiver
from django.http import JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.utils.functional import new_method_proxy
from django.views.generic import CreateView, ListView, View, UpdateView
from django.urls import reverse_lazy
from .forms import SignUpForm, UserUpdateForm
from .models import User,City
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from django.db.models import Case, When, Value, IntegerField
from matches.models import Match
from messenger.models import Message,Notification

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    model = User
    success_url = reverse_lazy('accounts:login')


class UserUpdateView(LoginRequiredMixin,UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('accounts:home')
    template_name = 'accounts/user_update.html'

    def get_object(self):
        return self.request.user






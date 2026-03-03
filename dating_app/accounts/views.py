from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import CreateView, ListView, View, UpdateView
from django.urls import reverse_lazy
from .forms import SignUpForm, UserUpdateForm
from .models import User,Match

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    model = User
    success_url = reverse_lazy('accounts:login')

class FeedView(ListView):
    template_name = 'feed/feedlist.html'
    model = User
    context_object_name = 'users'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = User.objects.all()
            swiped_users = Match.objects.filter(user_from = self.request.user).values_list('user_to',flat=True)
            queryset = queryset.exclude(id__in = swiped_users).exclude(id = self.request.user.id)
            return queryset
        else:
            return User.objects.all()


class MatchView(LoginRequiredMixin,View):
    def post(self,request,*args,**kwargs):
        current_status = Match.Status.SKIP
        user_id = kwargs.get('user_id')
        action = request.POST.get('action')
        target = get_object_or_404(User,id = user_id)
        if action == 'like':
            current_status = Match.Status.LIKE
            has_liked_back = Match.objects.filter(user_from=target,user_to = self.request.user,status = Match.Status.LIKE).exists()
        Match.objects.update_or_create(user_from = self.request.user,user_to = target,defaults ={'status':current_status})


        return redirect('accounts:home')


class MatchListView(ListView):
    model = User
    template_name = 'matches/match_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        liked = Match.objects.filter(user_from = self.request.user.id).values_list('user_to',flat=True)
        liked_me = Match.objects.filter(user_to = self.request.user.id).values_list('user_from',flat=True)
        same_ids = set(liked) & set(liked_me)

        return User.objects.filter(id__in = same_ids)


class UserUpdateView(LoginRequiredMixin,UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('accounts:home')
    template_name = 'accounts/user_update.html'

    def get_object(self):
        return self.request.user


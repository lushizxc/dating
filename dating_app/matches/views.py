from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Case, When, Value, IntegerField
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView,View
from accounts.models import User
from matches.models import Match
from messenger.models import Notification


class FeedView(LoginRequiredMixin,ListView):
    template_name = 'matches/feedlist.html'
    model = User
    context_object_name = 'users'

    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_authenticated:
            user_pref = self.request.user.interested_in
            queryset = User.objects.all()
            swiped_users = Match.objects.filter(user_from = self.request.user).values_list('user_to',flat=True)
            queryset = queryset.exclude(id__in = swiped_users).exclude(id = self.request.user.id)

            queryset = queryset.annotate(
                priority = Case(
                When(new_city=user.new_city,then=Value(1)),
                default=Value(2),
                output_field = IntegerField()
            ))

            if user_pref != "A":
                queryset = queryset.filter(gender = user_pref)

            return queryset.order_by('priority','?')
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



        Match.objects.update_or_create(user_from=self.request.user, user_to=target,defaults={'status': current_status})




        return redirect('accounts:home')


class MatchListView(ListView):
    model = User
    template_name = 'matches/match_list.html'
    context_object_name = 'users'

    def get(self, request, *args, **kwargs):
        notification = Notification.objects.filter(recipient = self.request.user,is_read = False).update(is_read = True)

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        liked = Match.objects.filter(user_from = self.request.user.id,status=Match.Status.LIKE).values_list('user_to',flat=True)
        liked_me = Match.objects.filter(user_to = self.request.user.id,status = Match.Status.LIKE).values_list('user_from',flat=True)
        same_ids = set(liked) & set(liked_me)

        return User.objects.filter(id__in = same_ids)


def unmatch(request,user_id):
    if request.method == 'POST':
        target_user = get_object_or_404(User,id = user_id)
        Match.objects.filter(user_from = request.user,user_to = target_user).update(status = Match.Status.SKIP)
    return redirect('accounts:matches')
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Case, When, Value, IntegerField
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View
from accounts.models import User
from matches.models import Match
from messenger.models import Notification


class FeedView(LoginRequiredMixin, ListView):
    template_name = 'matches/feedlist.html'
    model = User
    context_object_name = 'users'

    def get_queryset(self):
        user = self.request.user
        user_pref = user.interested_in

        queryset = User.objects.select_related('city').exclude(id=user.id)

        swiped_users = Match.objects.filter(user_from=user).values('user_to')
        queryset = queryset.exclude(id__in=swiped_users)

        queryset = queryset.annotate(
            priority=Case(
                When(city=user.city, then=Value(1)),
                default=Value(2),
                output_field=IntegerField()
            )
        )

        if user_pref != "A":
            queryset = queryset.filter(gender=user_pref)

        return queryset.order_by('priority', '?')[:15]


class MatchView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')

        if request.user.id == int(user_id):
            return redirect('matches:home')

        action = request.POST.get('action')
        target = get_object_or_404(User, id=user_id)

        current_status = Match.Status.LIKE if action == 'like' else Match.Status.SKIP

        Match.objects.update_or_create(
            user_from=request.user,
            user_to=target,
            defaults={'status': current_status}
        )
        return redirect('matches:home')

class MatchListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'matches/match_list.html'
    context_object_name = 'users'

    def get(self, request, *args, **kwargs):
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return User.objects.filter(
            swipes_received__user_from=self.request.user,
            swipes_received__status=Match.Status.LIKE,
            swipes_sent__user_to=self.request.user,
            swipes_sent__status=Match.Status.LIKE
        ).select_related('city').distinct()


def unmatch(request, user_id):
    if request.method == 'POST':
        target_user = get_object_or_404(User, id=user_id)

        match_obj = Match.objects.filter(user_from=request.user, user_to=target_user).first()
        if match_obj:
            match_obj.status = Match.Status.SKIP
            match_obj.save()

    return redirect('matches:matches')
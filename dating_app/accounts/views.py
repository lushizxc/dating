from django.contrib.auth.mixins import LoginRequiredMixin
from django.dispatch import receiver
from django.http import JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.utils.functional import new_method_proxy
from django.views.generic import CreateView, ListView, View, UpdateView
from django.urls import reverse_lazy
from .forms import SignUpForm, UserUpdateForm
from .models import User,Match,Message,Notification
from django.contrib import messages
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone



class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    model = User
    success_url = reverse_lazy('accounts:login')

class FeedView(LoginRequiredMixin,ListView):
    template_name = 'feed/feedlist.html'
    model = User
    context_object_name = 'users'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user_pref = self.request.user.interested_in
            queryset = User.objects.all()
            swiped_users = Match.objects.filter(user_from = self.request.user).values_list('user_to',flat=True)
            queryset = queryset.exclude(id__in = swiped_users).exclude(id = self.request.user.id).filter(city = self.request.user.city)

            if user_pref != "A":
                queryset = queryset.filter(gender = user_pref)

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

            if has_liked_back:
                messages.success(request, f'У тебя мэтч с {target.first_name} {target.last_name}!')

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


def chat(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        text_content = request.POST.get('text')

        try:
            last_msg = Message.objects.filter(sender=request.user, receiver=user).latest('created_at')
            if last_msg.text == text_content and (timezone.now() - last_msg.created_at).total_seconds() < 3:
                return JsonResponse({'error': 'message_spam', 'message': 'Слишком частая отправка'}, status=400)
        except Message.DoesNotExist:
            pass

        image = request.FILES.get('image')
        new_msg = Message.objects.create(
            text=text_content,
            receiver=user,
            sender=request.user,
            image=image
        )

        return JsonResponse({
            'id': new_msg.id,
            'text': new_msg.text,
            'sender': new_msg.sender.username,
            'created_at': new_msg.created_at.strftime("%H:%M"),
            'image_url': new_msg.image.url if new_msg.image and hasattr(new_msg.image, 'url') else None
        })

    last_id = request.GET.get('last_msg_id')
    if last_id:
        new_msgs = Message.objects.filter(
            Q(receiver=user_id, sender=request.user) | Q(sender=user_id, receiver=request.user),
            id__gt=last_id
        ).order_by('created_at')

        message_list = []
        for m in new_msgs:
            message_list.append({
                'id': m.id,
                'text': m.text,
                'sender': m.sender.username,
                'created_at': m.created_at.strftime("%H:%M"),
                'image_url': m.image.url if m.image and hasattr(m.image, 'url') else None
            })
        return JsonResponse({'messages': message_list})

    chat_messages = Message.objects.filter(
        Q(receiver=user_id, sender=request.user) | Q(sender=user_id, receiver=request.user)
    ).order_by('created_at')

    return render(request, 'accounts/chat.html', {
        'user': user,
        'chat_messages': chat_messages
    })
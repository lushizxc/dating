from datetime import *
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from accounts.models import User
from matches.models import Match
from .models import Message


def chat(request, user_id):
    partner = get_object_or_404(User, id=user_id)

    is_match = (
            Match.objects.filter(user_from=request.user, user_to=partner, status=Match.Status.LIKE).exists() and
            Match.objects.filter(user_from=partner, user_to=request.user, status=Match.Status.LIKE).exists()
    )
    if not is_match:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'no_match'}, status=403)
        return redirect('matches:home')

    if request.method == 'POST':
        text_content = request.POST.get('text')

        try:
            last_msg = Message.objects.filter(sender=request.user, receiver=partner).latest('created_at')
            if (timezone.now() - last_msg.created_at).total_seconds() < 1:
                return JsonResponse({'error': 'message_spam', 'message': 'Слишком частая отправка'}, status=400)
        except Message.DoesNotExist:
            pass

        image = request.FILES.get('image')

        if not text_content and not image:
            return JsonResponse({'error': 'empty_message', 'message': 'Пустое сообщение'}, status=400)

        new_msg = Message.objects.create(
            text=text_content, receiver=partner, sender=request.user, image=image
        )

        return JsonResponse({
            'id': new_msg.id,
            'text': new_msg.text,
            'sender': new_msg.sender.username,
            'created_at': new_msg.created_at.strftime("%H:%M"),
            'image_url': new_msg.image.url if new_msg.image else None
        })

    last_id = request.GET.get('last_msg_id')
    if last_id and str(last_id).isdigit():
        new_msgs = Message.objects.filter(
            Q(receiver=user_id, sender=request.user) | Q(sender=user_id, receiver=request.user),
            id__gt=int(last_id)
        ).select_related('sender').order_by('created_at')

        message_list = [{
            'id': m.id, 'text': m.text, 'sender': m.sender.username,
            'created_at': m.created_at.strftime("%H:%M"),
            'image_url': m.image.url if m.image else None
        } for m in new_msgs]
        return JsonResponse({'messages': message_list})

    chat_messages = Message.objects.filter(
        Q(receiver=user_id, sender=request.user) | Q(sender=user_id, receiver=request.user)
    ).select_related('sender').order_by('created_at')

    return render(request, 'messenger/chat.html', {'partner': partner, 'chat_messages': chat_messages})
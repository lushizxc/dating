from datetime import timezone

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from accounts.forms import User
from matches.models import Match
from .models import Message


def chat(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        text_content = request.POST.get('text')



        try:
            last_msg = Message.objects.filter(sender=request.user, receiver=user).latest('created_at')
            if (timezone.now() - last_msg.created_at).total_seconds() < 1:
                return JsonResponse({'error': 'message_spam', 'message': 'Слишком частая отправка'}, status=400)
        except Message.DoesNotExist:
            pass

        image = request.FILES.get('image')

        if not text_content and not image:
            return JsonResponse({'error': 'empty_message', 'message': 'Нельзя отправить пустое сообщение'}, status=400)
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

    is_match = Match.objects.filter(user_from = request.user,user_to = user,status = Match.Status.LIKE) and Match.objects.filter(user_from=user, user_to=request.user, status=Match.Status.LIKE)
    if not is_match:
        return redirect('accounts:home')

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

    return render(request, 'messenger/chat.html', {
        'user': user,
        'chat_messages': chat_messages
    })
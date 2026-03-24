from messenger.models import Notification

def notification(request):
    count = 0
    if request.user.is_authenticated:
        count = Notification.objects.filter(recipient = request.user,is_read = False).count()
        latest_notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')[:5]
        return {'unread_count':count,
                'recent_notifications': latest_notifications
                }
    return {}

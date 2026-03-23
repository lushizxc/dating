from .models import Notification

def notification(request):
    count = 0
    if request.user.is_authenticated:
        count = Notification.objects.filter(recipient = request.user,is_read = False).count()
    return {'unread_count':count}


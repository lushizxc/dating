from django.db.models.signals import post_save
from django.dispatch import receiver
from matches.models import Match
from messenger.models import Notification

@receiver(post_save, sender=Match)
def handle_match_notification(sender, instance, **kwargs):
    if instance.status == Match.Status.LIKE:
        reverse_match = Match.objects.filter(
            user_from=instance.user_to,
            user_to=instance.user_from,
            status=Match.Status.LIKE
        ).exists()

        if reverse_match:
            Notification.objects.get_or_create(
                recipient=instance.user_from,
                sender=instance.user_to,
                text=f"Take your time... Ты украл(а) сердце {instance.user_to.first_name}! Это взаимно."
            )
            Notification.objects.get_or_create(
                recipient=instance.user_to,
                sender=instance.user_from,
                text=f"Внимание! {instance.user_from.first_name} украл(а) твоё сердце! У вас мэтч."
            )
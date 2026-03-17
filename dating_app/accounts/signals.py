from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification, Match

print("РАЦИЯ ВКЛЮЧЕНА, СИГНАЛЫ ЗАГРУЖЕНЫ!")

@receiver(post_save,sender=Match)
def create_match_notification(sender,instance,created,**kwargs):
    if created:
        user_1 = instance.user_to
        user_2 = instance.user_from

        Notification.objects.create(
            recipient = user_1,
            sender = user_2,
            text = 'у вас мэтч'
        )


@receiver(post_save, sender=Match)
def create_match_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.user_to,
            sender=instance.user_from,
            text='У вас новый мэтч!'
        )
        Notification.objects.create(
            recipient=instance.user_from,
            sender=instance.user_to,
            text='У вас новый мэтч!'
        )
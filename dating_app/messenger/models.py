from django.db import models

from accounts.forms import User


class Message(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='messages_sent')
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name='messages_received')
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    image = models.ImageField(upload_to='chat_photos/',null=True,blank=True)

    class Meta:
        ordering = ['created_at',]

    def __str__(self):
        return f'{self.sender} -> {self.receiver}'

class Notification(models.Model):
    recipient = models.ForeignKey(User,on_delete=models.CASCADE,related_name='notification_received')
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='notification_sent')
    text = models.TextField(null = True,blank = True)
    is_read = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'from {self.sender} to {self.recipient}'


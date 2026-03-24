from django.db import models
from accounts.models import User



# Create your models here.
class Match(models.Model):
    class Status(models.TextChoices):
        SKIP = 'S','Пропустить'
        LIKE = 'L','Лайк'

    user_from = models.ForeignKey(User,on_delete=models.CASCADE,related_name='swipes_sent')
    user_to = models.ForeignKey(User,on_delete=models.CASCADE,related_name='swipes_received')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1,choices=Status.choices,default=Status.SKIP)

    class Meta:
        unique_together = (('user_from','user_to'),)
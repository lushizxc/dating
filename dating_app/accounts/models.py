from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import ForeignKey


class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = 'M','Мужчина'
        FEMALE = 'F','Женщина'

    avatar = models.ImageField(upload_to='avatars/',null=True,blank = True)
    gender = models.CharField(max_length=1,choices= Gender.choices,null=True,blank = True)
    bio = models.CharField(max_length=250,blank=True,default='')
    city = models.CharField(max_length=168,blank=False)
    date_of_birth = models.DateField(blank=False,null=True)

    REQUIRED_FIELDS = ['city','date_of_birth']

    def __str__(self):
        return self.username


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
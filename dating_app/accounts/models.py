from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import ForeignKey
from datetime import date

class User(AbstractUser):
    class Interstedin(models.TextChoices):
        ALL = 'A','Все'
        MALE = 'M','Мужчина'
        FEMALE = 'F','Женщина'

    class Gender(models.TextChoices):
        MALE = 'M','Мужчина'
        FEMALE = 'F','Женщина'

    avatar = models.ImageField(upload_to='avatars/',null=True,blank = True)
    gender = models.CharField(max_length=1,choices= Gender.choices,null=True,blank = True)
    bio = models.CharField(max_length=250,blank=True,default='')
    city = models.CharField(max_length=168,blank=False)
    date_of_birth = models.DateField(blank=False,null=True)
    interested_in = models.CharField(max_length=1,choices=Interstedin.choices,default=Interstedin.ALL)

    REQUIRED_FIELDS = ['city','date_of_birth']

    @property
    def age(self):
        if not self.date_of_birth:
            return "—"
        today = date.today()
        age = today.year - self.date_of_birth.year

        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1

        return age

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
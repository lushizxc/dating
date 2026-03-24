from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import ForeignKey
from datetime import date
from django.utils import timezone
from datetime import timedelta


class City(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name


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
    city = ForeignKey('City', null=True,on_delete=models.SET_NULL)
    bio = models.CharField(max_length=250,blank=True,default='')
    date_of_birth = models.DateField(blank=False,null=True)
    interested_in = models.CharField(max_length=1,choices=Interstedin.choices,default=Interstedin.ALL)
    last_seen = models.DateTimeField(blank = True,null = True)

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

    @property
    def is_online(self):
        if self.last_seen:
            return timezone.now() < self.last_seen + timedelta(minutes=5)
        return False


    def __str__(self):
        return self.username


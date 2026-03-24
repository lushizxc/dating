from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,City
from matches.models import Match
from messenger.models import Message,Notification

@admin.register(User)
class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        ('Мои дополнительные поля', {  # Название блока
            'fields': ('avatar', 'bio', 'city', 'date_of_birth', 'gender','interested_in')
        }),
    )

admin.site.register(Match)
admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(City)
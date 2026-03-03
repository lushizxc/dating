from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Match

@admin.register(User)
class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        ('Мои дополнительные поля', {  # Название блока
            'fields': ('avatar', 'bio', 'city', 'date_of_birth', 'gender')
        }),
    )

admin.site.register(Match)
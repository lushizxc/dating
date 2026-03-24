from . import views
from django.urls import path

urlpatterns = [
    path('chat/<int:user_id>/',views.chat,name='chat'),
]

app_name = 'messenger'

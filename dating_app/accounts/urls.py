from django.urls import path,include
from .views import SignUpView,FeedView,MatchView,MatchListView,UserUpdateView,chat
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('registration/',SignUpView.as_view(),name='registration'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('',FeedView.as_view(),name='home'),
    path('like/<int:user_id>/',MatchView.as_view(),name='match'),
    path('matches/',MatchListView.as_view(),name='matches'),
    path('update/',UserUpdateView.as_view(),name='update'),
    path('chat/<int:user_id>/',views.chat,name='chat'),
]

app_name = 'accounts'
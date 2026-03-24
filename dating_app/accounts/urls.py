from django.urls import path,include
from .views import SignUpView,UserUpdateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('registration/',SignUpView.as_view(),name='registration'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('update/',UserUpdateView.as_view(),name='update'),

]

app_name = 'accounts'
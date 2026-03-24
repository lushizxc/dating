from django.urls import path,include
from .views import FeedView,MatchView,MatchListView
from . import views
urlpatterns = [
    path('', FeedView.as_view(), name='home'),
    path('like/<int:user_id>/', MatchView.as_view(), name='match'),
    path('matches/', MatchListView.as_view(), name='matches'),
    path('unmatch/<int:user_id>/', views.unmatch, name='unmatch')

]

app_name = 'matches'
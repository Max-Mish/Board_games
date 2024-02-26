from django.urls import path

from .views import GameAPIView, CategoryAPIView, GamesAPIView, RelatedGamesAPIView

app_name = 'game'
urlpatterns = [
    path('', GamesAPIView.as_view(), name='games'),
    path('related', RelatedGamesAPIView.as_view(), name='related'),
    path('game/', GameAPIView.as_view(), name='game'),
    path('category/', CategoryAPIView.as_view(), name='category'),
]

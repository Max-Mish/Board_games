from django.urls import path

from .views import GameAPIView, CategoryAPIView, GamesAPIView, RelatedGamesAPIView, GameItemCreateAPIView, \
    DatesCheckAPIView, FullyBookedDaysAPIView

app_name = 'game'
urlpatterns = [
    path('', GamesAPIView.as_view(), name='games'),
    path('related', RelatedGamesAPIView.as_view(), name='related'),
    path('game/', GameAPIView.as_view(), name='game'),
    path('items/create/', GameItemCreateAPIView.as_view(), name='item create'),
    path('items/check_dates/', DatesCheckAPIView.as_view(), name='check dates'),
    path('items/disabled_dates/', FullyBookedDaysAPIView.as_view(), name='get disabled dates'),
    path('category/', CategoryAPIView.as_view(), name='category'),
]

from django.urls import path

from .views import GameAPIView, CategoryAPIView

app_name = 'game'
urlpatterns = [
    path('game/', GameAPIView.as_view(), name='game'),
    path('category/', CategoryAPIView.as_view(), name='category'),
]

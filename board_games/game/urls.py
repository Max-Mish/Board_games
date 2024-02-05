from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GameListViewSet

router = DefaultRouter()
router.register(r'game', GameListViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

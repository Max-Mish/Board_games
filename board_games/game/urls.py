from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import GamesViewSet

router = DefaultRouter()
router.register(r"games", GamesViewSet, basename="game")

urlpatterns = [
    path("", include(router.urls)),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserListViewSet, UserShortListViewSet

router = DefaultRouter()
router.register(r'user', UserListViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('user/short/', UserShortListViewSet.as_view())
]

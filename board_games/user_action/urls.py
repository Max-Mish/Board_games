from django.urls import path

from .views import BookingListViewSet, BookingFilteredViewSet

urlpatterns = [
    path('user_action/booking/', BookingListViewSet.as_view()),
    path('user_action/booking/filtered/', BookingFilteredViewSet.as_view())
]

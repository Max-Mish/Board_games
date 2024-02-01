from django.urls import path, include

from .views import BookingListViewSet, BookingFilteredViewSet

urlpatterns = [
    path('booking/', BookingListViewSet.as_view()),
    path('booking/filtered/', BookingFilteredViewSet.as_view())
]

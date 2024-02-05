from django.urls import path

from .views import BookingListViewSet, BookingFilteredViewSet, VoteListViewSet

urlpatterns = [
    path('user_action/booking/', BookingListViewSet.as_view()),
    path('user_action/booking/filtered/', BookingFilteredViewSet.as_view()),
    path('user_action/vote/', VoteListViewSet.as_view()),
]

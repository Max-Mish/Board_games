from django.urls import path

from .views import BookingAPIView, BookingFilteredAPIView, VoteAPIView

app_name = 'user_action'
urlpatterns = [
    path('user_action/booking/', BookingAPIView.as_view(), name='booking'),
    path('user_action/booking/filtered/', BookingFilteredAPIView.as_view(), name='booking_filtered'),
    path('user_action/vote/', VoteAPIView.as_view(), name='vote'),
]

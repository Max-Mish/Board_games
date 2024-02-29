from django.urls import path

from .views import BookingAPIView, BookingFilteredAPIView, VoteAPIView

app_name = 'user_action'
urlpatterns = [
    path('booking/', BookingAPIView.as_view(), name='booking'),
    path('booking/filtered/', BookingFilteredAPIView.as_view(), name='booking_filtered'),
    path('vote/', VoteAPIView.as_view(), name='vote'),
]

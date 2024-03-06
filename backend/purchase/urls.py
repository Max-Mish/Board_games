from django.urls import path

from payment_account.views import CallbackView
from .views import PurchaseItemView, DeliveryServiceAPIView

app_name = 'user_action'
urlpatterns = [
    path('purchase/', PurchaseItemView.as_view({'post': 'create'})),
    path('callback', CallbackView.as_view(), name='callback'),
    path('delivery_service/', DeliveryServiceAPIView.as_view(), name='delivery service'),
]

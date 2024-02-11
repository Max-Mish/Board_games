from django.urls import path

from .views import BalanceIncreaseAPIView, CalculatePaymentCommissionAPIView, CreatePaymentAcceptanceAPIView, \
    BalanceViewSet, UserCreateAPIView, YookassaPaymentAcceptanceView

app_name = 'payment_account'
urlpatterns = [
    path('increase_balance/', BalanceIncreaseAPIView.as_view(), name='increase_balance'),
    path('accept_payment/', YookassaPaymentAcceptanceView.as_view({'post': 'create'}), name='accept_payment'),
    path('payment_commission/', CalculatePaymentCommissionAPIView.as_view(), name='payment_commission'),
    # path('payment_acceptance/', CreatePaymentAcceptanceAPIView.as_view(), name='payment_acceptance'),
    path('create_account/', UserCreateAPIView.as_view(), name='create_account'),
    path('balances/', BalanceViewSet.as_view({'post': 'list'}), name='balances'),
    path('balances/<uuid:user_uuid>/', BalanceViewSet.as_view({'get': 'retrieve'}), name='balance'),
]

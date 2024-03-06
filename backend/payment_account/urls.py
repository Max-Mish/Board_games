from django.urls import path

from .views import BalanceIncreaseAPIView, CalculatePaymentCommissionAPIView, UserCreateAPIView, \
    YookassaPaymentAcceptanceView, BalancesAPIView, BalanceAPIView, CallbackView, PaymentServicesAPIView

app_name = 'payment_account'
urlpatterns = [
    path('increase_balance/', BalanceIncreaseAPIView.as_view(), name='increase_balance'),
    path('callback', CallbackView.as_view(), name='callback'),
    path('accept_payment/', YookassaPaymentAcceptanceView.as_view({'post': 'create'}), name='accept_payment'),
    path('payment_commission/', CalculatePaymentCommissionAPIView.as_view(), name='payment_commission'),
    path('payment_services/', PaymentServicesAPIView.as_view(), name='payment_services'),
    path('create_account/', UserCreateAPIView.as_view(), name='create_account'),
    path('balances/', BalancesAPIView.as_view(), name='balances'),
    path('balance/', BalanceAPIView.as_view(), name='my_balance'),
]

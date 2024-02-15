from django.urls import path

from .views import PurchaseItemView

app_name = 'user_action'
urlpatterns = [
    path('purchase/', PurchaseItemView.as_view({'post': 'create'})),
]

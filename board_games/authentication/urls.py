from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import RegistrationAPIView, MyTokenObtainPairView, ProfileAPIView

app_name = 'authentication'
urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegistrationAPIView.as_view(), name='auth_register'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),
]
